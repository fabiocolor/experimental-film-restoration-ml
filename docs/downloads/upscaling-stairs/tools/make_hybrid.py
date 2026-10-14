#!/usr/bin/env python3
"""Stairs kit, steps 1-2: the hybrid and the median carrier for one frame.

The 16 mm scan, median-filtered (23 px) and reduced to 240 x 135, gives the full
canvas. The nearest matching telecine frame (searched +/-12 frames) is registered
into scan coordinates with SIFT + RANSAC, tone-matched, and feathered in (48 px)
inside its picture area. The result is guide material for the reference still,
not a restored frame.

Usage:
  python make_hybrid.py --scan FG_01.00000200.png --telecine-dir BG_01/ \
      --telecine-pattern "BG_01.{:08d}.png" --frame 200 --last-frame 624 --out out/

Both inputs are 1920 x 1080 Rec.709 PNG frames. Writes f000200_hybrid_1920.png,
f000200_hybrid.png (768 x 432) and f000200_hybrid.json.
Ported from the research recipe used for the approved stairs shot (Q40).
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import cv2
import numpy as np

SEARCH_RADIUS = 12
ANALYSIS_SIZE = (768, 432)
RANSAC_THRESHOLD = 2.5
MIN_INLIERS = 18
MAX_MEDIAN_RESIDUAL = 2.5
MAX_P95_RESIDUAL = 5.0
FEATHER_PIXELS_FULL = 48


def rel(path: Path) -> str:
    return path.name


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise RuntimeError(f"Could not decode {path}")
    return image


def active_rectangle_mask(image: np.ndarray, inset: int = 5) -> tuple[np.ndarray, list[int]]:
    """Return the rectangular photographed support, excluding black padding."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    nonblack = gray > 4
    row_support = np.mean(nonblack, axis=1) > 0.04
    col_support = np.mean(nonblack, axis=0) > 0.04
    ys = np.flatnonzero(row_support)
    xs = np.flatnonzero(col_support)
    if len(xs) == 0 or len(ys) == 0:
        raise RuntimeError("Could not locate photographed image support")
    x0, x1 = int(xs[0]), int(xs[-1])
    y0, y1 = int(ys[0]), int(ys[-1])
    x0, y0 = x0 + inset, y0 + inset
    x1, y1 = x1 - inset, y1 - inset
    mask = np.zeros(gray.shape, dtype=np.uint8)
    mask[y0 : y1 + 1, x0 : x1 + 1] = 255
    return mask, [x0, y0, x1, y1]


def feature_gray(image: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (0, 0), 0.8)
    return cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(gray)


def normalized_correlation(left: np.ndarray, right: np.ndarray, mask: np.ndarray) -> float:
    valid = mask > 0
    if int(valid.sum()) < 1024:
        return -1.0
    a = left[valid].astype(np.float64)
    b = right[valid].astype(np.float64)
    a -= a.mean()
    b -= b.mean()
    denominator = float(np.linalg.norm(a) * np.linalg.norm(b))
    return float(np.dot(a, b) / denominator) if denominator > 1e-9 else -1.0


def robust_tone_match(telecine: np.ndarray, base: np.ndarray, mask: np.ndarray) -> tuple[np.ndarray, dict[str, float]]:
    tele_gray = cv2.cvtColor(telecine, cv2.COLOR_BGR2GRAY).astype(np.float32)
    base_gray = cv2.cvtColor(base, cv2.COLOR_BGR2GRAY).astype(np.float32)
    valid = mask > 0
    tele_values = tele_gray[valid]
    base_values = base_gray[valid]
    tele_p10, tele_p90 = np.percentile(tele_values, [10, 90])
    base_p10, base_p90 = np.percentile(base_values, [10, 90])
    scale = float((base_p90 - base_p10) / max(tele_p90 - tele_p10, 1.0))
    offset = float(base_p10 - scale * tele_p10)
    matched = np.clip(tele_gray * scale + offset, 0, 255).astype(np.uint8)
    return cv2.cvtColor(matched, cv2.COLOR_GRAY2BGR), {
        "scale": scale,
        "offset": offset,
        "telecine_p10": float(tele_p10),
        "telecine_p90": float(tele_p90),
        "base_p10": float(base_p10),
        "base_p90": float(base_p90),
    }


def register_candidate(
    scan_analysis: np.ndarray,
    base_analysis: np.ndarray,
    telecine_path: Path,
    target_frame: int,
    candidate_frame: int,
) -> dict[str, object] | None:
    tele_full = load(telecine_path)
    tele = cv2.resize(tele_full, ANALYSIS_SIZE, interpolation=cv2.INTER_AREA)
    tele_mask, bbox = active_rectangle_mask(tele, inset=6)
    scan_mask, _ = active_rectangle_mask(scan_analysis, inset=8)

    sift = cv2.SIFT_create(nfeatures=7000, contrastThreshold=0.018, edgeThreshold=14)
    kp_tele, des_tele = sift.detectAndCompute(feature_gray(tele), tele_mask)
    kp_scan, des_scan = sift.detectAndCompute(feature_gray(scan_analysis), scan_mask)
    if des_tele is None or des_scan is None:
        return None
    pairs = cv2.BFMatcher(cv2.NORM_L2).knnMatch(des_tele, des_scan, k=2)
    good = [a for a, b in pairs if a.distance < 0.72 * b.distance]
    if len(good) < 12:
        return None

    tele_points = np.float32([kp_tele[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    scan_points = np.float32([kp_scan[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    homography, inlier_mask = cv2.findHomography(
        tele_points,
        scan_points,
        cv2.RANSAC,
        RANSAC_THRESHOLD,
        maxIters=10000,
        confidence=0.999,
    )
    if homography is None or inlier_mask is None:
        return None
    inliers = inlier_mask.ravel().astype(bool)
    inlier_count = int(inliers.sum())
    if inlier_count < 8:
        return None

    projected = cv2.perspectiveTransform(tele_points[inliers], homography)
    residuals = np.linalg.norm(projected[:, 0, :] - scan_points[inliers, 0, :], axis=1)
    warped = cv2.warpPerspective(tele, homography, ANALYSIS_SIZE, flags=cv2.INTER_LANCZOS4)
    warped_support = cv2.warpPerspective(tele_mask, homography, ANALYSIS_SIZE, flags=cv2.INTER_NEAREST)
    comparison_mask = (warped_support > 0).astype(np.uint8) * 255
    roi = np.zeros(comparison_mask.shape, dtype=np.uint8)
    h, w = roi.shape
    roi[int(0.06 * h) : int(0.94 * h), int(0.18 * w) : int(0.79 * w)] = 255
    comparison_mask = cv2.bitwise_and(comparison_mask, roi)

    matched, _ = robust_tone_match(warped, base_analysis, comparison_mask)
    base_gray = cv2.cvtColor(base_analysis, cv2.COLOR_BGR2GRAY)
    matched_gray = cv2.cvtColor(matched, cv2.COLOR_BGR2GRAY)
    base_low = cv2.GaussianBlur(base_gray, (0, 0), 3.5)
    matched_low = cv2.GaussianBlur(matched_gray, (0, 0), 3.5)
    intensity_corr = normalized_correlation(base_low, matched_low, comparison_mask)
    base_grad = cv2.magnitude(
        cv2.Sobel(base_low, cv2.CV_32F, 1, 0),
        cv2.Sobel(base_low, cv2.CV_32F, 0, 1),
    )
    matched_grad = cv2.magnitude(
        cv2.Sobel(matched_low, cv2.CV_32F, 1, 0),
        cv2.Sobel(matched_low, cv2.CV_32F, 0, 1),
    )
    gradient_corr = normalized_correlation(base_grad, matched_grad, comparison_mask)
    median_residual = float(np.median(residuals))
    p95_residual = float(np.percentile(residuals, 95))
    # Same-instant appearance agreement dominates; feature support and residual
    # are secondary tie-breakers.  A tiny offset prior avoids choosing a remote
    # near-duplicate when the measured evidence is otherwise indistinguishable.
    selection_score = (
        0.72 * intensity_corr
        + 0.28 * gradient_corr
        + min(inlier_count, 100) * 0.0005
        - median_residual * 0.008
        - abs(candidate_frame - target_frame) * 0.0005
    )
    return {
        "target_scan_frame": target_frame,
        "candidate_telecine_frame": candidate_frame,
        "offset_frames": candidate_frame - target_frame,
        "telecine_path": rel(telecine_path),
        "feature_matches_after_ratio_test": len(good),
        "inliers": inlier_count,
        "inlier_fraction": float(inlier_count / len(good)),
        "median_residual_px_at_768x432": median_residual,
        "p95_residual_px_at_768x432": p95_residual,
        "low_frequency_intensity_correlation": intensity_corr,
        "low_frequency_gradient_correlation": gradient_corr,
        "selection_score": float(selection_score),
        "telecine_active_bbox_at_768x432": bbox,
        "homography_telecine_to_scan_at_768x432": homography.tolist(),
    }


def scale_homography(homography: np.ndarray, source_size: tuple[int, int]) -> np.ndarray:
    sx = source_size[0] / ANALYSIS_SIZE[0]
    sy = source_size[1] / ANALYSIS_SIZE[1]
    scale = np.array([[sx, 0.0, 0.0], [0.0, sy, 0.0], [0.0, 0.0, 1.0]])
    return scale @ homography @ np.linalg.inv(scale)




def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", type=Path, required=True)
    ap.add_argument("--telecine-dir", type=Path, required=True)
    ap.add_argument("--telecine-pattern", default="BG_01.{:08d}.png")
    ap.add_argument("--frame", type=int, required=True)
    ap.add_argument("--last-frame", type=int, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    frame = a.frame
    scan = load(a.scan)
    median = cv2.medianBlur(scan, 23)
    base = cv2.resize(cv2.resize(median, (240, 135), interpolation=cv2.INTER_AREA),
                      (1920, 1080), interpolation=cv2.INTER_LINEAR)
    sa = cv2.resize(scan, ANALYSIS_SIZE, interpolation=cv2.INTER_AREA)
    ba = cv2.resize(base, ANALYSIS_SIZE, interpolation=cv2.INTER_AREA)
    cands = []
    for n in range(max(1, frame - SEARCH_RADIUS), min(a.last_frame, frame + SEARCH_RADIUS) + 1):
        p = a.telecine_dir / a.telecine_pattern.format(n)
        if p.exists():
            r = register_candidate(sa, ba, p, frame, n)
            if r:
                cands.append(r)
    cands.sort(key=lambda r: r["selection_score"], reverse=True)
    best = cands[0] if cands else None
    ok = bool(best and best["inliers"] >= MIN_INLIERS
              and best["median_residual_px_at_768x432"] <= MAX_MEDIAN_RESIDUAL
              and best["p95_residual_px_at_768x432"] <= MAX_P95_RESIDUAL)
    row = {"frame": frame, "scan_sha256": sha(a.scan), "registration_pass": ok,
           "selected": best, "n_candidates": len(cands)}
    cv2.imwrite(str(a.out / f"f{frame:06d}_median_carrier.png"), base)
    if ok:
        tpath = a.telecine_dir / a.telecine_pattern.format(best["candidate_telecine_frame"])
        tele = load(tpath)
        h = scale_homography(np.asarray(best["homography_telecine_to_scan_at_768x432"]), (1920, 1080))
        support, _ = active_rectangle_mask(tele, inset=15)
        aligned = cv2.warpPerspective(tele, h, (1920, 1080), flags=cv2.INTER_LANCZOS4,
                                      borderMode=cv2.BORDER_CONSTANT)
        support = (cv2.warpPerspective(support, h, (1920, 1080), flags=cv2.INTER_NEAREST) > 127
                   ).astype(np.uint8) * 255
        toned, tone = robust_tone_match(aligned, base, support)
        alpha = np.clip(cv2.distanceTransform(support, cv2.DIST_L2, 5) / FEATHER_PIXELS_FULL, 0, 1
                        ).astype(np.float32)[:, :, None]
        hybrid = np.clip(base * (1 - alpha) + toned * alpha, 0, 255).astype(np.uint8)
        full = a.out / f"f{frame:06d}_hybrid_1920.png"
        small = a.out / f"f{frame:06d}_hybrid.png"
        cv2.imwrite(str(full), hybrid)
        cv2.imwrite(str(small), cv2.resize(hybrid, (768, 432), interpolation=cv2.INTER_AREA))
        row.update(telecine_sha256=sha(tpath), tone=tone, hybrid_1920_sha256=sha(full),
                   hybrid_768_sha256=sha(small))
    (a.out / f"f{frame:06d}_hybrid.json").write_text(json.dumps(row, indent=2, default=float) + "\n")
    print(frame, "pass" if ok else "FAIL: registration did not pass; pick another frame",
          best and best["candidate_telecine_frame"])


if __name__ == "__main__":
    main()
