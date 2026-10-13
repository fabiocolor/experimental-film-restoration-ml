#!/usr/bin/env python3
"""Make the three still inputs for the palette graph from one balanced frame.

  python prepare_still_inputs.py frame.png out_dir
writes source_y.png (the frame's own brightness, as grey), faded_frame.png (the frame itself, a weak colour hint)
and canny.png (edges, Canny 80/160). Load them into the three Load Image nodes of the palette graph.
"""
import shutil, sys
from pathlib import Path
import cv2
import numpy as np

src, out = Path(sys.argv[1]), Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
bgr = cv2.imread(str(src))
rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB).astype(np.float32) / 255
y = np.clip(np.rint((rgb @ np.array([.2126, .7152, .0722], np.float32)) * 255), 0, 255).astype(np.uint8)
cv2.imwrite(str(out / 'source_y.png'), np.repeat(y[..., None], 3, 2))
shutil.copyfile(src, out / 'faded_frame.png')
cv2.imwrite(str(out / 'canny.png'), cv2.cvtColor(cv2.Canny(cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY), 80, 160), cv2.COLOR_GRAY2BGR))
