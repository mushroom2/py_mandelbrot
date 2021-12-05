from PIL import Image, ImageDraw


# Image size (pixels)
WIDTH = 600
HEIGHT = 400
MAX_ITER = 80
# Plot window
RE_START = -2
RE_END = 1
IM_START = -1
IM_END = 1

palette = []

im = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
draw = ImageDraw.Draw(im)


def mandelbrot(c):
    z = 0
    n = 0
    while abs(z) <= 4 and n < MAX_ITER:
        z = z*z + c
        n += 1
    return n


for x in range(0, WIDTH):
    print(x)
    for y in range(0, HEIGHT):
        # Convert pixel coordinate to complex number
        c = complex(RE_START + (x / WIDTH) * (RE_END - RE_START),
                    IM_START + (y / HEIGHT) * (IM_END - IM_START))
        # Compute the number of iterations
        m = mandelbrot(c)
        # The color depends on the number of iterations
        color = 255 - int(m * 255 / MAX_ITER)
        # Plot the point
        draw.point([x, y], (color, color, color))

im.save('./data/bw_output.png', 'PNG')
