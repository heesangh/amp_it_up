


px = display.width/2
p_label = label.Label(FONT, text = "-------", color = 0x5555FF, x = int(px), y = display.height-5)
splash.append(p_label)

#ball hitbox x 0-5 y 2-7

bx = display.width/2
by = display.height*2/3
bvx = 0#60*2
bvy = -60*2


bi = []#brick info
for y in range(7):
    bi.append([])
    for x in range(11):
        bi[-1].append(y>1)#random.random()>0.5)

def gen_bricks():
    global bi
    bri = ""
    for y in range(len(bi)):
        for x in range(len(bi[y])):
            if(bi[y][x] or (y<len(bi)-1 and bi[y+1][x])):
                bri += "____"
            else:
                bri += "    "
            if(bi[y][x] or (x<len(bi[y])-1 and bi[y][x+1])):
                bri += "|"
            else:
                bri += " "
        bri += '\n'
    return bri

bricks = label.Label(FONT, text = gen_bricks() , color = 0xFFFFFF, x = 0, y = 5)
splash.append(bricks)

ball = label.Label(FONT, text = "o", color = 0xFFFF55, x = int(bx), y = int(by))
splash.append(ball)

lives = 3
life_label = label.Label(FONT, text = str(lives), color = 0xFF0000, x = 10, y = display.height-10)
splash.append(life_label)

lf = time.monotonic_ns()-10*6
cf = time.monotonic_ns()
running = True
while running:
    lf = cf
    cf = time.monotonic_ns()
    dt = min((cf-lf)/(10**9), 0.05)
    btn_poll() #reads buttons and creates events
    while(len(events)>0):
        events.pop(0)
    running= not (btns[0].value and btns[1].value and btns[2].value and btns[2].value)

    speed = (bvx**2+bvy**2)**0.5

    if(btns[2].value and px > 0):
        px -= speed*dt
    if(btns[3].value and px < display.width-41):
        px += speed*dt
    p_label.x = int(px)

    if(bx<0):
        bvx = abs(bvx)
    if(bx>display.width-5):
        bvx = -abs(bvx)

    if(by-2<0):
        bvy = abs(bvy)
    if(by+2+5>display.height):
        bvy = -abs(bvy)
        bvy *= 1.02
        bvx *= 1.02
        if(bx+4<px or bx>px+(7*6)):
            lives -= 1
            life_label.text = str(lives)
            bx = display.width/2
            by = display.height/3*2
            if(lives < 0):
                running = False
        else:
            mag = (bvx**2+bvy**2)**0.5
            thet = math.atan2(-20, -(px+(6*3.5))+(bx+2))
            bvx = math.cos(thet)*mag
            bvy = math.sin(thet)*mag

    bx += bvx*dt
    by += bvy*dt


    for i in range(len(bi[0])-1):
        thr = (i+1)*5*6-4
        if((bx-bvx*dt>thr) and (bx<thr)):#left hit
            bh = [int((by+4)//15), int((by+8)//15)]
            for h in bh:
                if(h<len(bi) and bi[h][i] == True):
                    bi[h][i] = False
                    bricks.text = gen_bricks()
                    bvx = abs(bvx)
            #time.sleep(0.5)
        thr -= 3
        if((bx-bvx*dt<thr) and (bx>thr)):#right hit
            bh = [int((by+4)//15), int((by+8)//15)]
            for h in bh:
                if(h<len(bi) and bi[h][i+1] == True):
                    bi[h][i+1] = False
                    bricks.text = gen_bricks()
                    bvx = -abs(bvx)
            #time.sleep(0.5)

    for i in range(len(bi)):
        thr = 15*(i+1)-4
        if((by-bvy*dt>thr) and (by<thr)):#top hit
            bh = [int((bx+4)//(5*6)), int((bx+7)//(5*6))]
            for h in bh:
                if(h<len(bi[0]) and bi[i][h] == True):
                    bi[i][h] = False
                    bricks.text = gen_bricks()
                    bvy = abs(bvy)
            #time.sleep(0.005)
        thr -= 4
        if((by-bvy*dt<thr) and (by>thr)):#bottom hit
            bh = [int((bx+4)//(5*6)), int((bx+8)//(5*6))]
            for h in bh:
                if(h<len(bi[0]) and i < len(bi)-1 and bi[i+1][h] == True):
                    bi[i+1][h] = False
                    bricks.text = gen_bricks()
                    bvy = -abs(bvy)
            #time.sleep(0.005)


    ball.x = int(bx)
    ball.y = int(by)

    display.refresh()

splash.remove(life_label)
splash.remove(p_label)
splash.remove(ball)
splash.remove(bricks)
del life_label
del p_label
del ball
del bricks
del bi
