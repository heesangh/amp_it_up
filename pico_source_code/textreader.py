# Write your code here :-)

lines_per = 16
text_lines = []


text_group = displayio.Group(scale = 1, x = 0, y = 0)
splash.append(text_group)

text_label = label.Label(FONT, text = "", color = 0xAAAAFF, x = 10, y = 15)
text_group.append(text_label)


os.chdir(working_directory)
with open(active_app, 'r') as file:
    for i in range(lines_per):
        text_lines.append(file.readline())
    text_string = ""
    for l in text_lines:
        text_string += "\n".join(wrap_text_to_lines(l, 50)) + '\n'
    text_label.text = text_string
    display.refresh()

    running = True
    while running:
        btn_poll()
        while(len(events) > 0):
            e = events.pop(0)
            if(e[0] == "left" and e[1] == True):
                running = False
            if(e[0] == "down" and e[1] == True):
                for i in range(8):
                    text_lines.pop(0)
                    text_lines.append(file.readline())
                text_string = ""
                for l in text_lines:
                    text_string += "\n".join(wrap_text_to_lines(l, 50)) + '\n'
                text_label.text = text_string
                display.refresh()
    del text_lines

splash.remove(text_group)
text_group.remove(text_label)

del text_group
del text_label





