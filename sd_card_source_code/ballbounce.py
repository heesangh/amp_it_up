

bx = display.width/2
by = display.height/2
bvx = 0
bvy = 0
grav = 80

ball = label.Label(FONT, text = 'o', x = int(bx), y = int(by))
splash.append(ball)

lf = time.monotonic_ns()-10*6
cf = time.monotonic_ns()
running = True
while running:
    lf = cf
    cf = time.monotonic_ns()
    dt = min((cf-lf)/(10**9), 0.05)
    btn_poll() #reads buttons and creates events
    running= not (btns[0].value and btns[1].value)
    while(len(events)>0):
        e = events.pop(0)
        if(e[0] == "up"    and e[1] == True):
            bvy -= 80
        if(e[0] == "down"  and e[1] == True):
            bvy += 80
        if(e[0] == "left"  and e[1] == True):
            bvx -= 80
        if(e[0] == "right" and e[1] == True):
            bvx += 80

    bvy += grav*dt

    bvx *= 0.9**dt
    bvy *= 0.9**dt

    bx += bvx*dt
    by += bvy*dt

    if(by-2<0):
        bvy = abs(bvy)
    if(by+4>display.height):
        bvy = -abs(bvy)
    if(bx<0):
        bvx = abs(bvx)
    if(bx+5>display.width):
        bvx = -abs(bvx)

    ball.x = int(bx)
    ball.y = int(by)

    display.refresh()

splash.remove(ball)
del ball


