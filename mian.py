from tkinter import *
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
CHECK_MARK = "✔"
marks = ""
app_timer = None


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global marks, reps
    window.after_cancel(app_timer)
    marks = ""
    reps = 0
    timer.config(text="Timer")
    check_mark.config(text=marks)
    canvas.itemconfig(timer_text, text="00:00")
    # when user press button the start button go in function mode again
    start_button.config(state=NORMAL)

    # Below code will make start button active again
    # refer to start_timer function to see why I disabled the button in first place
    start_button.config(state=NORMAL)


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps, marks
    reps += 1

    if reps % 8 == 0:
        count_down(LONG_BREAK_MIN*60)
        timer.config(text="Break", fg=RED)
        raise_above_all()

    elif reps % 2 == 0:
        count_down(SHORT_BREAK_MIN*60)
        timer.config(text="Break", fg=PINK)
        marks += CHECK_MARK
        check_mark.config(text=marks)
        raise_above_all()

    else:
        count_down(WORK_MIN*60)
        timer.config(text="Work", fg=GREEN)
    # The below code will fix the issue where user can press start multiple time and multiple session start at once
    # and user have to stop all the sessions manually
    # It will make button disable after user pressed the start button
    start_button.config(state=DISABLED)

    # It will fix the bug where you can start multiple
    # counter on top of each other and you have to manually reset them
    start_button.config(state=DISABLED)

# Creating function so window will pop-up from behind all the window and on the top when break will start
# ---------------------------- Pop-up window MECHANISM ------------------------------- #


def raise_above_all():
    # it will make window maximize in background if minimized 1st hand
    window.deiconify()
    # Note: Window will not get popped up infront if not maximized state already
    window.attributes('-topmost', 1)    # it will make the window popup
    # it makes window to let go him self back of the other window if we click on
    window.attributes('-topmost', 0)
    # other window or other window it will remain on the top and have to minimize manually


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

# use after method
# as creating simple loop with while loop to looping through code and changing break the code as the code is already in
# a loop
def count_down(count):
    minute_time = int((count-count % 60)/60)
    second_time = int(count % 60)

    # if you also want to add "00" to minute hand also
    # if second_time < 10 and minute_time < 10:
    #    canvas.itemconfig(timer_text, text=f"0{minute_time}:0{second_time}")
    if second_time < 10:
        canvas.itemconfig(timer_text, text=f"{minute_time}:0{second_time}")
    # elif minute_time < 10:
    #   canvas.itemconfig(timer_text, text=f"0{minute_time}:{second_time}")
    else:
        canvas.itemconfig(timer_text, text=f"{minute_time}:{second_time}")
    if count > 0:
        global app_timer
        app_timer = window.after(1000, count_down, count-1)

    # for testing purpose use 10 mili-second instead of 1000 mili-second so timer will run fast
    else:
        start_timer()
#     Finishing the project


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)


tomato_img = PhotoImage(file="tomato.png")
# pomo_icon = PhotoImage(file="pomo.png")


# Changing the title image of the app
window.iconphoto(False, tomato_img)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
# changing bg color and removing canvas thickness

canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(
    100, 130, text="00:00", fill="white", font=(FONT_NAME, 34, "bold"))
canvas.grid(column=1, row=1)

# count_down(5)

# Timer label
timer = Label(text="Timer", fg=GREEN, font=(FONT_NAME, 50), bg=YELLOW)
timer.grid(row=0, column=1)

# check mark label
check_mark = Label(fg=GREEN, bg=YELLOW)
check_mark.grid(row=3, column=1)

# Start button
start_button = Button(text="Start", bg=YELLOW,
                      highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2)

# Reset button
reset_button = Button(text="Reset", bg=YELLOW,
                      highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)


window.mainloop()
