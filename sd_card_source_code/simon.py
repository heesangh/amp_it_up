
up_label    = label.Label(FONT, text = "/ \\\n |\n |"       , x =   display.width//2-(6+3), y =   display.height//4-20, color = 0xFFFF00)
down_label  = label.Label(FONT, text = " |\n |\n\\ /"       , x =   display.width//2-(6+3), y = 3*display.height//4-20, color = 0x0000FF)
left_label  = label.Label(FONT, text = "/\n----\n\\"        , x =   display.width//4-(6+3), y =   display.height//2-20, color = 0x00FF00)
right_label = label.Label(FONT, text = "    \\\n----\n    /", x = 3*display.width//4-(6+3), y =   display.height//2-20, color = 0xFF0000)

arrow_labels = [down_label, up_label, left_label, right_label]

splash.append(   up_label)
splash.append( down_label)
splash.append( left_label)
splash.append(right_label)

hist = []
hist.append(random.randrange(0, 4))
point = len(hist)

speed = 0.5

time.sleep(0.3)
btn_poll()
while(len(events)>0):
    e = events.pop(0)


lf = time.monotonic_ns()-10*6
cf = time.monotonic_ns()
running = True
while running:
    lf = cf
    cf = time.monotonic_ns()
    dt = min((cf-lf)/(10**9), 0.05)
    btn_poll() #reads buttons and creates events
    running= not (btns[0].value and btns[1].value)
    if(point >= len(hist)):
        for l in arrow_labels:
            if l in splash:
                splash.remove(l)

        hist.append(random.randrange(0, 4))
        speed = (1/(len(hist)+5))**0.8*2
        for i in range(len(hist)):
            if(i >= len(hist)-2):
                speed = 0.3
            splash.append(arrow_labels[hist[i]])
            display.refresh()
            time.sleep(speed)
            splash.remove(arrow_labels[hist[i]])
            display.refresh()
            time.sleep(speed/2)
        time.sleep(0.1)
        point = 0

        for l in arrow_labels:
            splash.append(l)

    while(len(events)>0):
        e = events.pop(0)
        if(point >= len(hist) or running == False):
            break
        if(e[0] == "down"  and e[1] == False):
            if(hist[point] == 0):
                splash.remove(arrow_labels[0])
                display.refresh()
                time.sleep(speed/2)
                splash.append(arrow_labels[0])
                display.refresh()
                point += 1
            else:
                running = False
        if(e[0] == "up"    and e[1] == False):
            if(hist[point] == 1):
                splash.remove(arrow_labels[1])
                display.refresh()
                time.sleep(speed/2)
                splash.append(arrow_labels[1])
                display.refresh()
                point += 1
            else:
                running = False
        if(e[0] == "left"  and e[1] == False):
            if(hist[point] == 2):
                splash.remove(arrow_labels[2])
                display.refresh()
                time.sleep(speed/2)
                splash.append(arrow_labels[2])
                display.refresh()
                point += 1
            else:
                running = False
        if(e[0] == "right" and e[1] == False):
            if(hist[point] == 3):
                splash.remove(arrow_labels[3])
                display.refresh()
                time.sleep(speed/2)
                splash.append(arrow_labels[3])
                display.refresh()
                point += 1
            else:
                running = False



    display.refresh()

for l in arrow_labels:
    if(l in splash):
        splash.remove(l)

score_text = "score: " + str(len(hist)-1)
score_label = label.Label(FONT, text = score_text , x = (display.width-(len(score_text)*6))//2, y = (display.height-16)//2)
splash.append(score_label)
display.refresh()
running = True
while running:
    running= not (btns[0].value and btns[1].value)

splash.remove(score_label)



del score_text
del score_label
del    up_label
del  down_label
del  left_label
del right_label
del arrow_labels

