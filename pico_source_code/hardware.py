
import sys
import adafruit_sdcard
import board
import busio
import digitalio
import storage
import displayio
import adafruit_ili9341
import adafruit_ov5640

#from adafruit_rgb_display import color565
#import adafruit_rgb_display.ili9341 as ili9341

displayio.release_displays()
spi = busio.SPI(clock=board.GP2, MOSI=board.GP3, MISO=board.GP4)

display_bus = displayio.FourWire(spi, command=board.GP26, chip_select=board.GP1, reset=board.GP5, baudrate=80_000_000)
display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240, rotation=180)

sd_cs = digitalio.DigitalInOut(board.GP22)

try:
    sdcard = adafruit_sdcard.SDCard(spi, sd_cs)
except Exception:
    print("sd card init failed")
    while True:
        continue
while True:
    try:
        vfs = storage.VfsFat(sdcard)
        storage.mount(vfs, "/sd")
        sys.path.append("/sd")
        break
    except Exception:
        continue

with open("logo.txt", 'r') as file:
    lines = file.readlines()
    for line in lines:
        print(line, end='')
        time.sleep(0.05)
    print('')
display.auto_refresh = False

print("construct display bus")

splash = displayio.Group()
display.root_group = splash

print("construct i2c bus")
i2c = busio.I2C(board.GP9, board.GP8)

print("construct camera")
try:
    reset = digitalio.DigitalInOut(board.GP10)
    cam = adafruit_ov5640.OV5640(
        i2c_bus=i2c,
        data_pins=(board.GP12, board.GP13, board.GP14, board.GP15, board.GP16, board.GP17, board.GP18, board.GP19),
        clock=board.GP11,# pc
        vsync=board.GP7,
        href=board.GP21,
        mclk=board.GP20, #xc
        shutdown=None,
        reset=reset,
        size=adafruit_ov5640.OV5640_SIZE_QQVGA
    )

    print("chip id ", cam.chip_id)

    cam.colorspace = adafruit_ov5640.OV5640_COLOR_RGB
    cam.quality = 7

    cam.flip_y = True
    cam.flip_x = False
    cam.test_pattern = False
except Exception:
    print("camera init failed")
    while True:
        continue

print("construct buttons")

btns = [
    digitalio.DigitalInOut(board.GP0),
    digitalio.DigitalInOut(board.GP28),
    digitalio.DigitalInOut(board.GP27),
    digitalio.DigitalInOut(board.GP6)
    ]
for b in btns:
    b.switch_to_input(pull=digitalio.Pull.DOWN)


btn_states = []
for b in btns:
    btn_states.append(b.value)
events = []
btn_labels = ["down", "up", "left", "right"]

def btn_poll():
    for i in range(len(btns)):
        s = btns[i].value
        if(s != btn_states[i]):
            events.append((btn_labels[i], s))
        btn_states[i] = s

