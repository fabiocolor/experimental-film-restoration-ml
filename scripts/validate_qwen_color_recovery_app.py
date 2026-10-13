#!/usr/bin/env python3
"""Validate the public Qwen color recovery app package."""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path


EXPECTED_PROMPT = (
    "Recover stable RGB chroma for this faded film frame. Use image1 as the source shot and preserve its exact "
    "content, geometry, people, clothing, objects, framing, silhouettes, foreground/background layout, and spatial "
    "boundaries. Use image2 only as a soft color calibration field for period film hue relationships, natural skin "
    "color, believable foliage, sky, materials, clean neutrals, and restrained saturation. Use image3 as a hard "
    "source-derived edge map in the same geometry space as image1: follow those edges and boundaries closely so the "
    "recovered chroma stays aligned to the original luma after inverse mapping. Prioritize boundary alignment and "
    "composite usability over reconstructing texture or sharpness. Do not move faces, bodies, objects, buildings, "
    "sky lines, vehicles, or foreground/background borders. Do not redesign faces, add new objects, change the "
    "location, replace the scene, invent detail in blank skies, or copy visible chart content."
)

QWEN_NODE_TYPE = "cdb2cf24-c432-439b-b5c8-5f69838580c9"


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise AssertionError(f"{path}: cannot parse JSON: {exc}") from exc


def node_by_id(workflow: dict, node_id: int) -> dict:
    for node in workflow.get("nodes", []):
        if node.get("id") == node_id:
            return node
    raise AssertionError(f"missing node {node_id}")


def embedded_qwen_prompt(workflow: dict) -> str:
    for subgraph in workflow.get("definitions", {}).get("subgraphs", []):
        for node in subgraph.get("nodes", []):
            if str(node.get("id")) == "151":
                values = node.get("widgets_values") or []
                return str(values[0]) if values else ""
    raise AssertionError("missing embedded Qwen prompt node 151")


def validate_links(workflow: dict) -> None:
    nodes = {node["id"]: node for node in workflow.get("nodes", [])}
    links = {link[0]: link for link in workflow.get("links", [])}
    errors: list[str] = []
    for node in nodes.values():
        for input_slot in node.get("inputs") or []:
            link_id = input_slot.get("link")
            if link_id is not None and link_id not in links:
                errors.append(f"node {node['id']} input {input_slot.get('name')} references missing link {link_id}")
        for output_slot in node.get("outputs") or []:
            for link_id in output_slot.get("links") or []:
                if link_id not in links:
                    errors.append(f"node {node['id']} output {output_slot.get('name')} references missing link {link_id}")
    for link in links.values():
        if link[1] not in nodes:
            errors.append(f"link {link[0]} references missing source node {link[1]}")
        if link[3] not in nodes:
            errors.append(f"link {link[0]} references missing target node {link[3]}")
    if errors:
        raise AssertionError("; ".join(errors))


def validate_qwen_contract(workflow: dict) -> None:
    qwen = node_by_id(workflow, 170)
    if qwen.get("type") != QWEN_NODE_TYPE:
        raise AssertionError(f"node 170 is not Qwen Image Edit 2511: {qwen.get('type')}")
    inputs = {input_slot.get("name"): input_slot.get("link") for input_slot in qwen.get("inputs", [])}
    expected_inputs = {"image": 376, "image2": 377, "image3": 378}
    for name, link_id in expected_inputs.items():
        if inputs.get(name) != link_id:
            raise AssertionError(f"Qwen {name} should use link {link_id}, got {inputs.get(name)}")
    top_prompt = str((qwen.get("widgets_values") or [""])[0])
    subgraph_prompt = embedded_qwen_prompt(workflow)
    if top_prompt != EXPECTED_PROMPT:
        raise AssertionError("top-level Qwen prompt does not match the public recovery prompt")
    if subgraph_prompt != EXPECTED_PROMPT:
        raise AssertionError("embedded Qwen prompt does not match the recovery prompt")


def validate_source_reference_control(workflow: dict) -> None:
    source = node_by_id(workflow, 41)
    reference = node_by_id(workflow, 83)
    canny = node_by_id(workflow, 171)
    if source.get("type") != "LoadImage":
        raise AssertionError("node 41 must be a LoadImage source frame input")
    if reference.get("type") != "LoadImage":
        raise AssertionError("node 83 must be a LoadImage color reference input")
    if (reference.get("widgets_values") or [""])[0] != "faded-color-reference-palette.png":
        raise AssertionError("node 83 must load the included colour reference palette")
    if canny.get("type") != "Canny":
        raise AssertionError("node 171 must generate Canny from the source frame")
    if canny.get("widgets_values") != [0.4, 0.8]:
        raise AssertionError(f"Canny thresholds should be [0.4, 0.8], got {canny.get('widgets_values')}")


def validate_outputs(workflow: dict) -> None:
    save_nodes = [node for node in workflow.get("nodes", []) if node.get("type") == "SaveImage"]
    prefixes = {(node.get("widgets_values") or [""])[0] for node in save_nodes}
    required = {"Faded_Color_Recovery_Raw_Inference", "Faded_Color_Recovery_Composite"}
    if "Faded_Color_Recovery_Cloud_Composite" in prefixes:
        required.remove("Faded_Color_Recovery_Composite")
        required.add("Faded_Color_Recovery_Cloud_Composite")
    missing = required - prefixes
    if missing:
        raise AssertionError(f"missing SaveImage outputs: {sorted(missing)}")


def validate_cloud_workflow(workflow: dict) -> None:
    disallowed = {"FadedSourceLumaChromaComposite", "LoadVideo", "GetVideoComponents", "ImageFromBatch"}
    node_types = {node.get("type") for node in workflow.get("nodes", [])}
    forbidden = sorted(disallowed & node_types)
    if forbidden:
        raise AssertionError(f"Cloud workflow contains non-Cloud-safe nodes: {forbidden}")
    for required in {"GetImageSize", "ImageScale", "ImageRGBToYUV", "ImageYUVToRGB"}:
        if required not in node_types:
            raise AssertionError(f"Cloud workflow missing built-in composite node: {required}")
    if "ResizeImageMaskNode" in node_types:
        raise AssertionError("Cloud workflow uses ResizeImageMaskNode, whose widget layout breaks on ComfyUI Cloud; use GetImageSize + ImageScale")
    for node in workflow.get("nodes", []):
        if node.get("type") == "ImageScale" and (node.get("widgets_values") or [None])[0] != "lanczos":
            raise AssertionError("Cloud ImageScale must use lanczos")
    extra = workflow.get("extra", {}).get("faded_color_recovery", {})
    if extra.get("cloud_safe") is not True or extra.get("custom_nodes_required") is not False:
        raise AssertionError("Cloud workflow metadata must mark cloud_safe true and custom_nodes_required false")


def validate_local_workflow(workflow: dict) -> None:
    node_types = {node.get("type") for node in workflow.get("nodes", [])}
    if "FadedSourceLumaChromaComposite" not in node_types:
        raise AssertionError("local workflow must include the full final-composite helper")


def validate_zip(repo: Path, files: list[Path]) -> None:
    zip_path = repo / "docs/downloads/faded-qwen-color-recovery-app.zip"
    if not zip_path.is_file():
        raise AssertionError(f"missing package zip: {zip_path}")
    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
        required_entries = [
            "qwen-color-recovery/README.md",
            "qwen-color-recovery/THIRD_PARTY_NOTICES.md",
            "qwen-color-recovery/assets/faded-color-reference-palette.png",
            "qwen-color-recovery/assets/demo_unbalanced_source_frame.jpg",
            "qwen-color-recovery/workflows/faded-qwen-2511-cloud-composite-app.json",
            "qwen-color-recovery/workflows/faded-qwen-2511-still-composite-app.json",
            "qwen-color-recovery/custom_nodes/faded_color_recovery/__init__.py",
        ]
        missing = [entry for entry in required_entries if entry not in names]
        if missing:
            raise AssertionError(f"zip missing entries: {missing}")
        for file_path in files:
            relative_name = file_path.relative_to(repo / "docs/downloads/qwen-color-recovery").as_posix()
            archive_name = "qwen-color-recovery/" + relative_name
            if archive.read(archive_name) != file_path.read_bytes():
                raise AssertionError(f"zip entry is stale: {archive_name}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    repo = args.repo.resolve()
    package_root = repo / "docs/downloads/qwen-color-recovery"
    cloud_path = package_root / "workflows/faded-qwen-2511-cloud-composite-app.json"
    local_path = package_root / "workflows/faded-qwen-2511-still-composite-app.json"
    assets = [
        package_root / "assets/faded-color-reference-palette.png",
        package_root / "assets/demo_unbalanced_source_frame.jpg",
    ]
    package_docs = [
        package_root / "README.md",
        package_root / "THIRD_PARTY_NOTICES.md",
    ]
    for path in [cloud_path, local_path, *assets, *package_docs]:
        if not path.exists():
            raise AssertionError(f"missing package file: {path}")

    cloud = load_json(cloud_path)
    local = load_json(local_path)
    for name, workflow in [("cloud", cloud), ("local", local)]:
        validate_links(workflow)
        validate_qwen_contract(workflow)
        validate_source_reference_control(workflow)
        validate_outputs(workflow)
        print(f"OK {name}: graph, prompt, inputs, Canny, outputs")
    validate_cloud_workflow(cloud)
    print("OK cloud: portable built-in composite path present")
    validate_local_workflow(local)
    print("OK local: full final-composite helper present")
    validate_zip(repo, [cloud_path, local_path, *assets, *package_docs])
    print("OK package zip: required files present and workflow entries are current")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
