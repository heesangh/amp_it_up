# SPDX-FileCopyrightText: Copyright (c) 2023 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""
This demo is designed for the Raspberry Pi Pico. with 240x240 SPI TFT display

It shows the camera image on the LCD
"""
import time
import busio
import board
import digitalio
import adafruit_ov5640
import adafruit_ili9341
import displayio
import sdcardio
import storage
import adafruit_bitmapsaver
import os

# Set up the display (You must customize this block for your display!)
displayio.release_displays()


print("construct display bus")
spi = busio.SPI(clock=board.GP2, MOSI=board.GP3, MISO=board.GP4)

print("construct SD card bus")
sd_cs = board.GP22
sdcard = sdcardio.SDCard(spi, sd_cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

display_bus = displayio.FourWire(spi, command=board.GP26, chip_select=board.GP1, reset=board.GP5)
display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240, rotation=0)



print("construct bus")
i2c = busio.I2C(board.GP9, board.GP8)

print("construct camera")
reset = digitalio.DigitalInOut(board.GP10)
cam = adafruit_ov5640.OV5640(
    i2c_bus=i2c,
    data_pins=(
        board.GP12,
        board.GP13,
        board.GP14,
        board.GP15,
        board.GP16,
        board.GP17,
        board.GP18,
        board.GP19
    ),
    clock=board.GP11,# pc
    vsync=board.GP7,
    href=board.GP21,
    mclk=board.GP20, #xc
    shutdown=None,
    reset=reset,
    size=adafruit_ov5640.OV5640_SIZE_96X96
)

print("print chip id")
print(cam.chip_id)

cam.colorspace = adafruit_ov5640.OV5640_COLOR_RGB

cam.flip_y = False
cam.flip_x = False
cam.test_pattern = False

width = display.width
height = display.height

bitmap = displayio.Bitmap(cam.width, cam.height, 65535)
print(width, height, cam.width, cam.height)
if bitmap is None:
    raise SystemExit("Could not allocate a bitmap")


g = displayio.Group(scale=1, x=(width-cam.width)//2, y=(height-cam.height)//2)
tg = displayio.TileGrid(bitmap,
    pixel_shader=displayio.ColorConverter(input_colorspace=displayio.Colorspace.RGB565_SWAPPED)
)

g.append(tg)

display.root_group = g

t0 = time.monotonic_ns()
display.auto_refresh = False

#while True:
cam.capture(bitmap)
bitmap.dirty()
display.refresh()

old_size = cam.size
old_colorspace = cam.colorspace

cam.size = adafruit_ov5640.OV5640_SIZE_VGA
cam.colorspace = adafruit_ov5640.OV5640_COLOR_JPEG
b = bytearray(cam.capture_buffer_size)
jpeg = cam.capture(b)
with open('/sd/image.jpg', 'wb') as f:
    f.write(jpeg)
    f.close()

print("Image saved")

list = os.listdir('/sd/')

for l in list:
    print(list)


cam.size = old_size
cam.colorspace = old_colorspace

