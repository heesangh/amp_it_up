# Write your code here :-)



running = True
os.chdir(working_directory)

try:
    image, palette = adafruit_imageload.load(active_app, bitmap=displayio.Bitmap, palette=displayio.Palette)
except Exception:
    running = False


if running:
    image_grid = displayio.TileGrid(image, pixel_shader=palette)

    g = displayio.Group(scale = 2, x = (display.width-image.width*2)//2, y = (display.height-image.height*2)//2)
    g.append(image_grid)
    splash.append(g)


    display.refresh()

    while running:
        btn_poll()
        while(len(events) > 0):
            e = events.pop(0)
            if(e[0] == "left" and e[1] == True):
                running = False




    g.remove(image_grid)
    splash.remove(g)

    del image
    del palette
    del image_grid
    del g





