from itertools import cycle
from random import randrange
from tkinter import Canvas, Tk, messagebox, font

canvas_width = 800
canvas_height = 400

root = Tk()   # creates a window
c = Canvas(root, width=canvas_width, height=canvas_height, background="deep sky blue")  # the canvas will be sky blue & measure 800x400 px
c.create_rectangle(-5, canvas_height-100, canvas_width+5, canvas_height+5, fill="sea green", width=0)  # this creates the grass
c.create_oval(-80, -80, 120, 120, fill='orange', width=0)  # creates the sun
c.pack()  # pack() func tells the program to draw the main window and all of its contents.

color_cycle = cycle(["light blue", "light green", "light pink", "light yellow", "light cyan"])  # cycle func allows u to use each color in turn.
egg_width = 45
egg_height = 55
egg_score = 10  # you score 10 points for catching an egg.
egg_speed = 100
egg_interval = 4000  # a new egg appears after every 4000 millisec (4sec).
difficulty = 0.95  # this is how much the speed & interval chnge after each catch .
catcher_color = "blue"
catcher_width = 100
catcher_height = 100  # height of the circle  used to draw the arc.
catcher_startx = canvas_width / 2 - catcher_width / 2
catcher_starty = canvas_height - catcher_height - 20
catcher_startx2 = catcher_startx + catcher_width
catcher_starty2 = catcher_starty + catcher_height  # these lines make the catcher start near the bottom of the canvas, in the center of the window.

catcher = c.create_arc(catcher_startx, catcher_starty,  \
                       catcher_startx2, catcher_starty2, start=200, extent=140,    # start drawing at 200 deg on the circle and draw for 140 degrees.
                       style='arc', outline=catcher_color , width=3)  # to draw the catcher

game_font = font.nametofont("TkFixedFont")  # selects a cool computer-style font.
game_font.config(size=18)  # make text larger or smaller by changing this number.


score = 0
score_text = c.create_text(10, 10, anchor="nw", font=game_font, fill="darkblue", text="Score: "+ str(score))

lives_remaining = 3  # the player gets  3 lives
lives_text = c.create_text(canvas_width-10, 10, anchor="ne", font=game_font, fill="darkblue", text="Lives: "+ str(lives_remaining))

eggs = []  # this is the list to keep track of the eggs.

def create_egg():
    x = randrange(10, 740)  #to pick a random position along the top of the canvas for the new egg.
    y = 40
    new_egg = c.create_oval(x, y, x+egg_width, y+egg_height, fill=next(color_cycle), width=0)  # creates th oval
    eggs.append(new_egg)  #shape is added to the list of eggs.
    root.after(egg_interval, create_egg)  # call this func again after the no. of millisec stored in egg_interval.

def move_eggs():
    for egg in eggs:
        (eggx, eggy, eggx2, eggy2) = c.coords(egg)  # gets each egg's coordinates.
        c.move(egg, 0, 10)  # egg drops down the screen 10 px at a time.
        if eggy2 > canvas_height:  # to check if the egg is at the bottom of the screen.
            egg_dropped(egg)  # if so, call the func that deals with dropped eggs.
    root.after(egg_speed, move_eggs)  # call this func again after the no. of millisec stored in egg_speed.

def egg_dropped(egg):
    eggs.remove(egg)  # egg is removed from the eggs list.
    c.delete(egg)  # the egg disappears from the canvas.
    lose_a_life()
    if lives_remaining == 0:
        messagebox.showinfo("Game Over!", "Final Score: "+ str(score))  # if no lives are left, tell the player that the game is over.
        root.destroy()  # the game ends.

def lose_a_life():
    global lives_remaining  # this variable needs to be global, as the func will modify  it.
    lives_remaining -= 1
    c.itemconfigure(lives_text, text="Lives: "+ str(lives_remaining))  # updates the text that shows the remaining lives.

def check_catch():
    (catcherx, catchery, catcherx2, catchery2) = c.coords(catcher)
    for egg in eggs:
        (eggx, eggy, eggx2, eggy2) = c.coords(egg)
        if catcherx < eggx and eggx2 < catcherx2 and catchery2 - eggy2 < 40:  # check is the egg inside the catcher horizontally & vertically.
            eggs.remove(egg)
            c.delete(egg)
            increase_score(egg_score)  # increases the score by 10 points
    root.after(100, check_catch)  # calls this func again aftter 100 millisec (1/10th of a sec).

def increase_score(points):
    global score, egg_speed, egg_interval
    score += points
    egg_speed = int(egg_speed * difficulty)
    egg_interval = int(egg_interval * difficulty)
    c.itemconfigure(score_text, text="Score: "+ str(score))

def move_left(event):
    (x1, y1, x2, y2) = c.coords(catcher)
    if x1 > 0:  # has the catcher reached the left wall
        c.move(catcher, -20, 0)  # if not move the catcher left

def move_right(event):
    (x1, y1, x2, y2) = c.coords(catcher)
    if x2 < canvas_width:  # has the catcher reached the right wall
        c.move(catcher, 20, 0)  # if not, move the catcher right

c.bind("<Left>", move_left)
c.bind("<Right>", move_right)
c.focus_set()
root.after(1000, create_egg)  # the 3 game loops begin
root.after(1000, move_eggs)   # after slight pause of
root.after(1000, check_catch)  # 1000 millisec (1sec)
root.mainloop()  # starts the main tkinter loop.