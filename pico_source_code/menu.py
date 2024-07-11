
os.chdir(working_directory)

menu_items = []
action_items = []
selected = False
if("menu_point" not in globals()):
    menu_point = 0
if("menu_scroll" not in globals()):
    menu_scroll = 0
ndisp = 13
action_point = 0
running = True




def open_item(item):
    global selected, running, active_app, working_directory, menu_point
    selected = False
    if(os.stat(item)[0]>>14 == 1):
        dir_hist.append(os.getcwd())
        os.chdir(item)
        menu_point = 0
        print("changed directory to : ", item)
    elif(os.stat(item)[0]>>14 == 2 and (item[-3:] == ".py" or item[-4:] == ".txt" or item[-4:] == ".bmp")):
        active_app = item
        working_directory = os.getcwd()
        running = False

def copy_to_sd(item):
    global selected
    copy_directory = os.getcwd()
    with open(item, 'rb') as file:
        os.chdir(base_directory)
        os.chdir("sd")
        with open(item, 'wb') as dest_file:
            dest_file.write(file.read())

    os.chdir(copy_directory)
    print("copied ", item, " to sd card")
    selected = False

def copy_to_pico(item):
    copy_directory = os.getcwd()
    with open(item, 'rb') as file:
        os.chdir(base_directory)
        with open(item, 'wb') as dest_file:
            dest_file.write(file.read())
    os.chdir(copy_directory)
    print("copied ", item, " to pico")


def delete_item(item):
    global selected, menu_point
    os.remove(item)
    selected = False
    if(menu_point >= len(menu_items)):
        menu_point = len(menu_items)-1
    print("removed ", item)


action_items.append(("open", lambda : open_item(menu_items[menu_point])))
action_items.append(("to sd", lambda : copy_to_sd(menu_items[menu_point])))
action_items.append(("to pico", lambda : copy_to_pico(menu_items[menu_point])))
action_items.append(("delete", lambda : delete_item(menu_items[menu_point])))


menu_group = displayio.Group(scale=1, x=0, y=0)
splash.append(menu_group)

menu_bitmap = displayio.Bitmap(0, 0, 1)#display.width, display.height)
menu_palette = displayio.Palette(1)
menu_palette[0] = 0x000000
menu_sprite = displayio.TileGrid(menu_bitmap, x = 0, y = 0, pixel_shader = menu_palette)
menu_group.append(menu_sprite)

xo = 30
yo = 30

menu_text = label.Label(FONT, text = "menu", color = 0x00FF00, x = 0+xo, y = 5+yo)
menu_group.append(menu_text)

action_text = label.Label(FONT, text = "actions", color = 0x0000FF, x = 140+xo, y = 5+yo)
menu_group.append(action_text)

menu_pointer = label.Label(FONT, text = "<", color = 0xFF0000, x = 120+xo, y = 5+yo)
menu_group.append(menu_pointer)

action_pointer = label.Label(FONT, text = "<", color = 0xFF0000, x = 200+xo, y = 5+yo)
menu_group.append(action_pointer)

def update_menu_items():
    global menu_items
    excluded = ["System Volume Information", "boot_out.txt", "lib", "hardware.py", "logo.txt", "main.py", "menu.py", "textreader.py", "bmpreader.py"]
    menu_items = os.listdir()
    i = 0
    while(i < len(menu_items)):
        if(menu_items[i][0] == '.' or menu_items[i] in excluded):
            menu_items.pop(i)
            continue
        else:
            i += 1

def update_menu():
    global action_text, action_pointer, action_point, menu_text, menu_pointer, menu_point
    #action_text.hidden = not selected
    if(not selected):
        mt = ""
        for i in range(menu_scroll, min(menu_scroll+ndisp, len(menu_items))):
            mt += menu_items[i] + '\n'
        menu_text.text = mt

        mpt = ""
        for i in range(menu_scroll, menu_point):
            mpt += '\n'
        mpt += '<'
        menu_pointer.text = mpt

        action_text.text = " "
        action_pointer.text = " "
    else:
        at = ""
        for i in range(min(menu_point-menu_scroll, ndisp-4)):
            at += '\n'
        for i in range(len(action_items)):
            at += action_items[i][0] + '\n'
        action_text.text = at

        apt = ""
        for i in range(action_point+min(menu_point-menu_scroll, ndisp-4)):
            apt += '\n'
        apt += '<'
        action_pointer.text = apt

update_menu_items()
update_menu()
display.refresh()
while running:

    #if(b1.value and b2.value and b3.value and b4.value):
    #    break
    btn_poll()

    while(len(events)>0):
        e = events.pop(0)
        #print(e)
        if(e[0] == "down" and e[1] == True):
            if(not selected):
                menu_point  = min((menu_point+1), len(menu_items)-1)
                if(menu_point>=menu_scroll+ndisp-1 and menu_scroll < len(menu_items)-ndisp):
                    menu_scroll += 1
            else:
                action_point = (action_point+1)%len(action_items)

        if(e[0] == "up" and e[1] == True):
            if(not selected):
                menu_point = max(menu_point-1, 0)
                if(menu_point<= menu_scroll and menu_scroll > 0):
                    menu_scroll -= 1
            else:
                action_point = (action_point-1+len(action_items))%len(action_items)

        if(e[0] == "left" and e[1] == True):
            if(not selected):
                if(len(dir_hist)>0):
                    os.chdir(dir_hist.pop(-1))
                    update_menu_items()
            else:
                selected = False

        if(e[0] == "right" and e[1] == True):
            if(not selected):
                selected = True
                action_point = 0
            elif(menu_point < len(menu_items)):
                action_items[action_point][1]()
                update_menu_items()

        if(e[0] in btn_labels and e[1] == True):
            update_menu()
        #print(menu_items)
        #print(menu_point)


    #menu_text.text = a[random.randint(0, 6)] + '\n' + a[random.randint(0, 6)] + '\n' + a[random.randint(0, 6)] + '\n'
    display.refresh()

menu_group.remove(action_text)
menu_group.remove(menu_text)
menu_group.remove(action_pointer)
menu_group.remove(menu_pointer)
menu_group.remove(menu_sprite)
splash.remove(menu_group)

del action_text
del menu_text
del action_pointer
del menu_pointer
del menu_sprite
del menu_group






