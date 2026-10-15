"""Cineon / ADX10 film log -> Rec.709 display, applied as a view transform ("as is", no look).
Kodak Cineon log: black 95/1023, white 685/1023, 0.002 density per code value, negative gamma 0.6.
"""
import numpy as np
from PIL import Image
def cineon_to_linear(x, black=95, white=685, gamma=0.6):
    cv = x * 1023.0
    off = 10 ** ((black - white) * 0.002 / gamma)
    lin = (10 ** ((cv - white) * 0.002 / gamma) - off) / (1 - off)
    return np.clip(lin, 0, None)
def rec709_oetf(l):
    l = np.clip(l, 0, 1)
    return np.where(l < 0.018, 4.5 * l, 1.099 * np.power(l, 0.45) - 0.099)
def apply(im):
    a = np.asarray(im.convert('RGB')).astype(np.float32) / 255
    return Image.fromarray((np.clip(rec709_oetf(cineon_to_linear(a)), 0, 1) * 255 + 0.5).astype(np.uint8))
def write_cube(path, n=4096):
    x = np.linspace(0, 1, n); y = np.clip(rec709_oetf(cineon_to_linear(x)), 0, 1)
    with open(path, 'w') as f:
        f.write('TITLE "Cineon log to Rec709 view"\nLUT_1D_SIZE %d\n' % n)
        for v in y: f.write('%.6f %.6f %.6f\n' % (v, v, v))
if __name__ == '__main__':
    import sys
    write_cube('cineon_to_rec709.cube')
    for p in sys.argv[1:]:
        im = Image.open(p); out = apply(im); out.save(p.rsplit('/', 1)[-1].rsplit('.', 1)[0] + '-709.jpg', quality=90)
