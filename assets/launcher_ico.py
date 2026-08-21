#--------------------------------

# Imports
from PIL import Image
import math
from pathlib import Path

output_path = Path(__file__).resolve().parent / ".." / "launcher" / "assets" / "launcher.ico"
output_path.parent.mkdir(parents=True, exist_ok=True)
#--------------------------------

CYAN = [0, 255, 255]
PINK = [255, 20, 190]

size = 256
img = Image.new("RGBA", (size, size))
pixels = img.load()
cx = cy = (size-1)/2

# Outer ring
for y in range(size):
    for x in range(size):
        dx = x - cx
        dy = -y + cy

        r = math.sqrt(dx*dx + dy*dy)
        t = min(r / (size/2), 1.0)
        if t == 1 or t < 0.85 or abs(dx) < 13:
            #print(t)
            continue

        tx = 2*dx/(size-1)
        ty = 2*dy/(size-1)
        theta = math.atan(ty/tx)+math.pi/2
        #print("tx=", tx, " and ty=", ty, " theta=",theta)

        q = theta/math.pi
        if q < 0:
            q *= -1
            red = int(PINK[0] * (1 - q) + CYAN[0] * q)
            green = int(PINK[1] * (1 - q) + CYAN[1] * q)
            blue = int(PINK[2] * (1 - q) + CYAN[2] * q)
        else:
            red = int(CYAN[0] * (1 - q) + PINK[0] * q)
            green = int(CYAN[1] * (1 - q) + PINK[1] * q)
            blue = int(CYAN[2] * (1 - q) + PINK[2] * q)

        pixels[x, y] = (red, green, blue, 255)
#--------------------------------


# Inner ring
for y in range(size):
    for x in range(size):
        dx = x - cx
        dy = -y + cy

        r = math.sqrt(dx*dx + dy*dy)
        t = min(r / (size/2), 1.0)
        if t > 0.75 or t < 0.6 or abs(dy) < 10:
            #print(t)
            continue

        tx = 2*dx/(size-1)
        ty = 2*dy/(size-1)
        theta = math.atan(ty/tx)
        #print("tx=", tx, " and ty=", ty, " theta=",theta)

        q = theta/math.pi
        if q < 0:
            q *= -1
            red = int(PINK[0] * (1 - q) + CYAN[0] * q)
            green = int(PINK[1] * (1 - q) + CYAN[1] * q)
            blue = int(PINK[2] * (1 - q) + CYAN[2] * q)
        else:
            red = int(CYAN[0] * (1 - q) + PINK[0] * q)
            green = int(CYAN[1] * (1 - q) + PINK[1] * q)
            blue = int(CYAN[2] * (1 - q) + PINK[2] * q)

        pixels[x, y] = (red, green, blue, 255)
#--------------------------------

# And save it
img.save(
    output_path,
    sizes=[
        (16, 16),
        (24, 24),
        (32, 32),
        (48, 48),
        (64, 64),
        (128, 128),
        (256, 256),
    ]
)
#--------------------------------

