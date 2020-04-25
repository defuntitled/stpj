from colour import Color
from PIL import ImageDraw, ImageFont, Image


def generate_cover(sid, aid, grad):
    img = Image.new("RGBA", (1920, 1080))
    im = img.load()
    x, y = img.size
    if grad == 0:
        col = Color('#9D00B9')
        colors = list(map(lambda x: x.rgb, col.range_to(Color("blue"), 1920)))
    elif grad == 1:
        col = Color('#9D00B9')
        colors = list(map(lambda x: x.rgb, col.range_to(Color("white"), 1920)))
    elif grad == 2:
        col = Color('#9D00B9')
        colors = list(map(lambda x: x.rgb, col.range_to(Color((74, 186, 87)), 1920)))
    for i in range(x):
        for j in range(y):
            im[i, j] = (int(colors[i][0]), int(colors[i][1]), int(colors[i][2]))

    img.save(f"data/{aid}/{sid}_cover.png")

generate_cover(1, 1, 0)
