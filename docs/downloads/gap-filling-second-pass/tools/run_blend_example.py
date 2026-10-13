"""The second-pass example: windows W1 0-80, W2 51-131, W3 102-182 at 768x560, cuts at 57 and 114.

  CWC_INPUT_DIR=<folder with W1.mkv W2.mkv W3.mkv> CWC_OUTPUT_DIR=out python run_blend_example.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import seam_blend  # noqa: E402
sys.argv = ['seam_blend.py', '--layout', 'full560', '--window', 'w1:0:W1.mkv:81:560', '--window', 'w2:51:W2.mkv:81:560', '--window', 'w3:102:W3.mkv:81:560',
            '--cut', '57:w1:w2', '--cut', '114:w2:w3', '--dissolve', '16', '--label', 'r25']
seam_blend.main()
