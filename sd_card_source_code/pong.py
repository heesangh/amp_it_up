# Write your code here :-)

rel_text = label.Label(FONT, text = "release", color = 0x00FF00, x = 10, y = display.height-20)

p1y = display.height/2-25
p2y = display.height/2-25

p1 = label.Label(FONT, text = "|\n|\n|\n|", color = 0x88FF88, x = 2, y = int(p1y))
p2 = label.Label(FONT, text = "|\n|\n|\n|", color = 0xFF8888, x = display.width-5, y = int(p2y))

p1s = 0
p2s = 0

p1s_text = label.Label(FONT, text = str(p1s), color = 0xFF88FF, x = display.width//4, y = 20)
p2s_text = label.Label(FONT, text = str(p2s), color = 0x88FFFF, x = 3*display.width//4, y = 20)


ball = label.Label(FONT, text = "o", color = 0x8888FF, x = display.width//2, y = display.height//2)
bvx = 60
bvy = 60
bx = ball.x
by = ball.y

lb = False

parti = []
parti_label = []
parti_n = 10
for i in range(parti_n):
    parti.append([-10, -10, 0, 0])#x, y, vx, vy
    parti_label.append(label.Label(FONT, text = '.', color = 0xFFFF88, x = 0, y = 0))
    splash.append(parti_label[-1])

splash.append(p1)
splash.append(p2)
splash.append(p1s_text)
splash.append(p2s_text)
splash.append(ball)


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
    running= not (btns[0].value and btns[1].value)

    ps = (bvx**2+bvy**2)**0.5*0.7
    if(btns[1].value and p1y>5):
        p1y -= ps*dt
    if(btns[0].value and p1y<display.height-50):
        p1y += ps*dt

    if(by<p2y+25 and p2y>5):
        p2y -= 60*dt
    if(by>p2y+25 and p2y<display.height-50):
        p2y += 60*dt

    p1.y = int(p1y)
    p2.y = int(p2y)

    bx += bvx*dt
    by += bvy*dt
    if(bx-5<0):
        bvx = abs(bvx)
        if(by+4<p1y-5 or by-2>p1y+50):
            p2s += 1
            p2s_text.text = str(p2s)
            bx = display.width/2
            by = display.height/2
        elif(lb):
            for i in range(parti_n):
                thet = random.uniform(-math.pi/2+0.3, math.pi-0.3)
                mag = random.uniform(10, 30)
                parti[i][2] = math.cos(thet)*mag
                parti[i][3] = math.sin(thet)*mag
                parti[i][0] = bx-5+parti[i][2]*0.5
                parti[i][1] = by+1+parti[i][3]*0.5
            bvx *= 1.02
            bvy *= 1.02
            thet = math.atan2(by-(p1y+25), 20)
            mag = (bvx**2+bvy**2)**0.5
            bvx = math.cos(thet)*mag
            bvy = math.sin(thet)*mag
        lb = False


    if(bx+3+5>display.width):
        bvx = -abs(bvx)
        if(by+4<p2y-5 or by-2>p2y+50):
            p1s += 1
            p1s_text.text = str(p1s)
            bx = display.width/2
            by = display.height/2
        elif(not lb):
            for i in range(parti_n):
                thet = random.uniform(math.pi/2+0.3, 3/2*math.pi-0.3)
                mag = random.uniform(10, 30)
                parti[i][2] = math.cos(thet)*mag
                parti[i][3] = math.sin(thet)*mag
                parti[i][0] = bx+3+parti[i][2]*0.5
                parti[i][1] = by+1+parti[i][3]*0.5
            bvx *= 1.02
            bvy *= 1.02
            thet = math.atan2(by-(p2y+25), -20)
            mag = (bvx**2+bvy**2)**0.5
            bvx = math.cos(thet)*mag
            bvy = math.sin(thet)*mag
        lb = True


    if(by-2<0):
        bvy = abs(bvy)
    if(by+4>display.height):
        bvy = -abs(bvy)

    ball.x = int(bx)
    ball.y = int(by)

    for i in range(parti_n):
        parti[i][0] += parti[i][2]*dt
        parti[i][1] += parti[i][3]*dt
        parti_label[i].x = int(parti[i][0])
        parti_label[i].y = int(parti[i][1])



    display.refresh()

for i in range(parti_n):
    splash.remove(parti_label[i])

del parti_label
del parti

splash.remove(p1)
splash.remove(p2)
splash.remove(p1s_text)
splash.remove(p2s_text)
splash.remove(ball)
del p1
del p2
del p1s_text
del p2s_text
del ball
