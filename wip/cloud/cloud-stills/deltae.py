#!/usr/bin/env python3
"""Mean CIEDE2000-free ΔE (CIE76 in Lab, OpenCV float) between two images: deltae.py a.png b.png"""
import sys,cv2,numpy as np
def lab(p):
    im=cv2.imread(p,cv2.IMREAD_COLOR).astype(np.float32)/255.0
    return cv2.cvtColor(im,cv2.COLOR_BGR2Lab)
a,b=lab(sys.argv[1]),lab(sys.argv[2])
if a.shape!=b.shape: b=cv2.resize(b,(a.shape[1],a.shape[0]),interpolation=cv2.INTER_AREA)
d=np.sqrt(((a-b)**2).sum(-1))
print(f"meanΔE76={d.mean():.3f} p95={np.percentile(d,95):.3f} max={d.max():.2f}")
