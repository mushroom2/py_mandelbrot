from PIL import Image
import colorsys
import numpy as np
import time
px, py = -0.7746806106269039, -0.1374168856037867  # Tante Renate
max_iteration = 30
w, h = 1000, 1000
mfactor = 0.5
maxiter_const = mfactor / max_iteration ** mfactor
minx, maxx, miny, maxy = 0, w - 1, 0, h - 1
global RX1, RX2, RY1, RY2


def mandelbrot2(x, y, max_iteration):

    c = complex((x - minx) / (maxx - minx) * (RX2 - RX1) + RX1,
                (y - miny) / (maxy - miny) * (RY2 - RY1) + RY1)
    i = 0
    z = 0
    while abs(z) <= 2 and i <= max_iteration:
        z = z*z + c
        i += 1
    return i


def mandelbrot(x, y, max_iteration):
    zx = 0
    zy = 0
    RX1, RX2, RY1, RY2 = px - R / 2, px + R / 2, py - R / 2, py + R / 2
    cx = (x - minx) / (maxx - minx) * (RX2 - RX1) + RX1
    cy = (y - miny) / (maxy - miny) * (RY2 - RY1) + RY1
    i = 0
    while zx ** 2 + zy ** 2 <= 4 and i < max_iteration:
        temp = zx ** 2 - zy ** 2
        zy = 2 * zx * zy + cy
        zx = temp + cx
        i += 1
    return i


def gen_Mandelbrot_image(sequence):
    c_accum = None
    v_accum = None
    bitmap = Image.new("RGB", (w, h), "white")
    pix = bitmap.load()
    for x in range(w):
        avg_fractal = []
        for y in range(h):
            b_frac = time.time()
            c = mandelbrot2(x, y, max_iteration)
            a_frac = round(time.time() - b_frac, 3)
            avg_fractal.append(a_frac)
            v = c ** maxiter_const if c != c_accum else v_accum
            c_accum = c
            v_accum = v
            hv = 0.67 - v
            if hv < 0:
                hv += 1
            r, g, b = colorsys.hsv_to_rgb(hv, 1, 1 - (v - 0.1) ** 2 / 0.9 ** 2)
            r = min(255, round(r * 255))
            g = min(255, round(g * 255))
            b = min(255, round(b * 255))
            pix[x, y] = int(r) + (int(g) << 8) + (int(b) << 16)
        print(x, round(np.average(avg_fractal), 3))
    bitmap.save("./data/Mandelbrot_" + str(sequence) + ".png")


R = 3
f = 0.975
RZF = 1 / 1000000000000
k = 1
while R > RZF:
    if k > 100:
        break
    mfactor = 0.5 + (1 / 1000000000000) ** 0.1 / R ** 0.1
    print(k, mfactor)
    RX1, RX2, RY1, RY2 = px - R / 2, px + R / 2, py - R / 2, py + R / 2
    gen_Mandelbrot_image(k)
    R *= f
    k += 1
