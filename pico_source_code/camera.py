# SPDX-FileCopyrightText: Copyright (c) 2023 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""
This demo is designed for the Raspberry Pi Pico. with 240x240 SPI TFT display

It shows the camera image on the LCD
"""

cap_text = label.Label(FONT, text = "capturing", color = 0x00FF00, x = 10, y = display.height-50)
sav_text = label.Label(FONT, text = "saving", color = 0x00FF00, x = 10, y = display.height-35)
rel_text = label.Label(FONT, text = "release", color = 0x00FF00, x = 10, y = display.height-20)

bitmap = displayio.Bitmap(cam.width, cam.height, 2**16-1)
if bitmap is None:
    raise SystemExit("Could not allocate a bitmap")

scale = 1
g = displayio.Group(scale = scale, x = 0, y = 0)
tg = displayio.TileGrid(bitmap, pixel_shader=displayio.ColorConverter(input_colorspace=displayio.Colorspace.RGB565_SWAPPED), x = (display.width-cam.width*scale)//2, y = (display.height-cam.height*scale)//2)
g.append(tg)

splash.append(g)

#cap_size = adafruit_ov5640.OV5640_SIZE_QQVGA
#cap_col = adafruit_ov5640.OV5640_COLOR_JPEG
#old_size = cam.size
#old_col = cam.colorspace
#cam.size, cam.colorspace = cap_size, cap_col
#buffer = bytearray(cam.capture_buffer_size)
#buffer = displayio.Bitmap(cam.width, cam.height, 2**16-1)
#print("capture size: ", cam.capture_buffer_size)
#cam.size, cam.colorspace = old_size, old_col


t0 = time.monotonic_ns()
lf = time.monotonic_ns()
cam.capture(bitmap)

running = True
while running:
    cf = time.monotonic_ns()
    lf=cf
    cap = False

    btn_poll()
    while(len(events) > 0):
        e = events.pop(0)
        if(e[0] == "left" and e[1] == True):
            running = False
        if(e[0] == "up" and e[1] == True):
            cap = True

    if(not cap):
        cam.capture(bitmap)
        bitmap.dirty()
        display.refresh()
    else:
        g.append(cap_text)
        display.refresh()

        #cam.size, cam.colorspace = cap_size, cap_col


        cam.capture(bitmap)

        sav_text.text = "saving"
        g.append(sav_text)
        display.refresh()

        cam_directory = os.getcwd()
        os.chdir(base_directory)
        os.chdir("sd")
        if("pics" not in os.listdir()):
            os.mkdir("pics")
        os.chdir("pics")

        files = os.listdir()
        for i in range(len(files)):
            if((files[i][-4:] != ".jpg" and files[i][-4:] != ".bmp") or files[i][:4] != "img_"):
                print(files[i])
                files.pop(i)
                continue
            try:
                files[i] = int(files[i][4:-4])
            except ValueError:
                files.pop(i)
                continue
        print(files)
        if(len(files) == 0):
            files.append(-1)

        sav_text.text = "saving - " + "img_{:06d}.bmp".format(max(files)+1)
        display.refresh()
        adafruit_bitmapsaver.save_pixels("img_{:06d}.bmp".format(max(files)+1), bitmap, displayio.ColorConverter(input_colorspace=displayio.Colorspace.RGB565_SWAPPED))
        #with open("img_{:06d}.jpg".format(max(files)+1), "wb") as f:
        #    f.write(buffer)

        os.chdir(cam_directory)

        g.append(rel_text)
        display.refresh()
        time.sleep(0.1)

        g.remove(cap_text)
        g.remove(sav_text)
        g.remove(rel_text)
        display.refresh()

        #cam.size, cam.colorspace = old_size, old_col


g.remove(tg)
splash.remove(g)

del cap_text
del sav_text
del rel_text
del bitmap
#del jpeg
del tg
del g

