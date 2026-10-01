#!/usr/bin/env python3
"""Compute WCAG 2.x contrast ratio between two colors.

Usage: contrast.py FG BG [--size PX] [--bold true|false]
Colors: #rgb, #rrggbb, rgb(r,g,b), rgba(r,g,b,a) (alpha is composited over BG).
Prints the ratio and which common thresholds it meets. A measurement aid, not a compliance audit.
"""
import re, sys, argparse

def parse(c, bg=None):
    c = c.strip().lower()
    if c.startswith('#'):
        h = c[1:]
        if len(h) == 3: h = ''.join(x*2 for x in h)
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    m = re.match(r'rgba?\(([^)]+)\)', c)
    if not m: raise ValueError(f'Unsupported color: {c}')
    p = [float(x) for x in re.split(r'[,\s/]+', m.group(1).strip()) if x]
    r, g, b = p[:3]
    a = p[3] if len(p) > 3 else 1.0
    if a < 1 and bg: r, g, b = [a*f + (1-a)*k for f, k in zip((r, g, b), bg)]
    return (r, g, b)

def lum(rgb):
    def f(v):
        v /= 255
        return v/12.92 if v <= 0.03928 else ((v+0.055)/1.055) ** 2.4
    r, g, b = map(f, rgb)
    return 0.2126*r + 0.7152*g + 0.0722*b

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('fg'); ap.add_argument('bg')
    ap.add_argument('--size', type=float, default=16, help='font size in px')
    ap.add_argument('--bold', default='false')
    a = ap.parse_args()
    bg = parse(a.bg); fg = parse(a.fg, bg)
    l1, l2 = sorted((lum(fg), lum(bg)), reverse=True)
    ratio = (l1 + 0.05) / (l2 + 0.05)
    bold = a.bold.lower() == 'true'
    large = a.size >= 24 or (bold and a.size >= 18.66)
    need = 3.0 if large else 4.5
    print(f'ratio: {ratio:.2f}:1')
    print(f'text ({"large" if large else "normal"}) needs {need}:1 -> {"meets" if ratio >= need else "BELOW"} reference threshold')
    print(f'non-text UI (3:1) -> {"meets" if ratio >= 3 else "BELOW"}')
    print('AAA text (7:1 normal / 4.5:1 large) -> ' + ('meets' if ratio >= (4.5 if large else 7) else 'below'))

if __name__ == '__main__':
    try: main()
    except Exception as e:
        print(f'error: {e}', file=sys.stderr); sys.exit(1)
