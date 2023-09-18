from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pygame
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

# Pygarm mixer init (you should always init the mixier module to play the sound)
pygame.mixer.init()

# -------------------- MUSIC LOAD & START FUNCTION ----------------------- #


def music_start():
    # Below code will load the music and play that after pressing start
    pygame.mixer.music.load(filename="audio/audio.mp3")    # To Load the music
    # To play the music loop=-1 will play music indefinietly
    pygame.mixer.music.play(loops=-1)
    # Ddefault volume set to 0.3 so it wont start very loud
    # After trial and error I get this value, and feels perfect match for me 0.0375
    pygame.mixer.music.set_volume(0.0375)


# ---------------- MUSIC START & START BUTTON FUNCTION ------------------ #

def music_timer_start():
    # Below code will merge the music_start function and start_timer funtion
    music_start()
    start_timer()


# ----------------------SETTING VOLUME WITH SLIDER ------------------------ #
def set_volume(x):
    current_voulume = volume_slider.get()
    # As I select slider from 0-100 so dividing the value as pygame support value between 0-1 only (and I need very low sound)
    # If you need high sound decrease the number to 100 so it will give actual value from 0-1
    set_volume = current_voulume/300
    pygame.mixer.music.set_volume(set_volume)

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

    # stop the music when user press reset timer
    pygame.mixer.music.stop()


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps, marks
    reps += 1

    if reps % 8 == 0:
        count_down(LONG_BREAK_MIN*60)
        timer.config(text="Break", fg=RED)
        raise_above_all()
        pygame.mixer.music.pause()  # It will pause the music when break start

    elif reps % 2 == 0:
        count_down(SHORT_BREAK_MIN*60)
        timer.config(text="Break", fg=PINK)
        marks += CHECK_MARK
        check_mark.config(text=marks)
        raise_above_all()
        pygame.mixer.music.pause()  # It will pause the music when break start

    else:
        count_down(WORK_MIN*60)
        timer.config(text="Work", fg=GREEN)
        pygame.mixer.music.unpause()  # It will resume the music when break start
        messagebox.showinfo(title="Healthy Instructions",
                            message="Please wear your computer glasses, then start your work.\nTake a sip of water before starting anything.")

    # The below code will fix the issue where user can press start multiple time and multiple session start at once
    # and user have to stop all the sessions manually
    # It will make button disable after user pressed the start button
    start_button.config(state=DISABLED)

    # # Below code will load the music and play that after pressing start
    # pygame.mixer.music.load(filename="audio.mp3")    # To Load the music
    # pygame.mixer.music.play()                        # To play the music

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
        app_timer = window.after(10, count_down, count-1)

    # for testing purpose use 10 mili-second instead of 1000 mili-second so timer will run fast
    else:
        start_timer()
#     Finishing the project

# ---------------------------- TIMER SETTING------------------------------- #


def session_timer(option):
    setting_window.destroy()
    global WORK_MIN, SHORT_BREAK_MIN, LONG_BREAK_MIN

    if option == "thirty":
        WORK_MIN = 30
        SHORT_BREAK_MIN = 5
        LONG_BREAK_MIN = 20

    elif option == "fortyfive":
        WORK_MIN = 45
        SHORT_BREAK_MIN = 5
        LONG_BREAK_MIN = 30

    elif option == "sixty":
        WORK_MIN = 60
        SHORT_BREAK_MIN = 10
        LONG_BREAK_MIN = 60

    else:
        WORK_MIN = 25
        SHORT_BREAK_MIN = 5
        LONG_BREAK_MIN = 20


def timer_setting():
    global setting_window  # We have to make it global so we can access outside of the fuction to close automatically after pressing any button
    setting_window = Toplevel(window)  # Toplevel is way to make popup window
    setting_window.title("Timer setting")
    setting_window.config(padx=20, pady=20, bg=YELLOW)

    # Setting button
    # for selecting different window for adding button in it add name of the wondow at the start of the creating button
    default_button = Button(setting_window, text="Default", bg=YELLOW,
                            highlightthickness=0, command=lambda: session_timer("default"))
    default_button.grid(column=1, row=1)

    # 30/5/20 button
    thirty_button = Button(setting_window, text="30/5/20", bg=YELLOW,
                           highlightthickness=0, command=lambda: session_timer("thirty"))
    thirty_button.grid(column=2, row=1)

    # 45/5/30 button
    thirty_button = Button(setting_window, text="45/5/30", bg=YELLOW,
                           highlightthickness=0, command=lambda: session_timer("fortyfive"))
    thirty_button.grid(column=1, row=2)

    # 60/10/60 button
    thirty_button = Button(setting_window, text="60/10/60", bg=YELLOW,
                           highlightthickness=0, command=lambda: session_timer("sixty"))
    thirty_button.grid(column=2, row=2)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("PomoFi")
window.config(padx=100, pady=50, bg=YELLOW)


tomato_img = PhotoImage(file="images/tomato.png")
# pomo_icon = PhotoImage(file="pomo.png")


# Changing the title image of the app
window.iconphoto(True, tomato_img)

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

# Start button with 2 function will start timer and music
start_button = Button(text="Start", bg=YELLOW,
                      highlightthickness=0, command=music_timer_start)
start_button.grid(column=0, row=2)

# Reset button
reset_button = Button(text="Reset", bg=YELLOW,
                      highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)

# Volume Slider

style = ttk.Style()
style.configure("TScale", background=YELLOW)
volume_slider = ttk.Scale(
    from_=0, to=100, orient=HORIZONTAL, value=12, length=180, style="TScale", command=set_volume)
volume_slider.grid(column=1, row=4)


# Volume label
volume_lable = Label(text="Volume", bg=YELLOW)
volume_lable.grid(row=5, column=1)

# Setting button
setting_button = Button(text="Setting", bg=YELLOW,
                        highlightthickness=0, command=timer_setting)
setting_button.grid(column=1, row=6)

window.mainloop()
