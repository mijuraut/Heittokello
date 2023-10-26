from tkinter import *
import time
import winsound


# -------------------------------- CONSTANTS -------------------------------- #
SHOT_CLOCK_FULL = 24
SHOT_CLOCK_FRONTCOURT = 14
SHOT_CLOCK_START_SHOWING_DECIMALS_AT = 5
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
is_running = False
time_remaining_sec = 24.0
timer = None
INTEGER_FONT = (FONT_NAME, 30, "bold")
DECIMAL_FONT = (FONT_NAME, 20, "bold")

# -------------------------------- PLAY SOUND -------------------------------- #
def play_sound():
    winsound.PlaySound("SystemAsterisk", winsound.SND_ASYNC)


# -------------------------------- TIMER PAUSE -------------------------------- #
def pause_timer():
    global is_running
    is_running = False


# -------------------------------- TIMER RESET -------------------------------- #
def reset_timer():
    global time_remaining_sec, is_running, timer

    # Reset pressed during game (ball touches rim for example) or we're at 0.0 seconds.
    if is_running or (canvas.itemcget(timer_text, 'text') == "0.0" and timer is not None):
        # Stop the countdown, empty screen
        window.after_cancel(timer)
        is_running = False
        canvas.itemconfig(timer_text, text="")
    # clock is not running, clock is not visible
    elif canvas.itemcget(timer_text, 'text') == "":
        time_remaining_sec = SHOT_CLOCK_FRONTCOURT
        canvas.itemconfig(timer_text, text=f"{time_remaining_sec}")
    else:
        # Set the timer text to an empty string
        canvas.itemconfig(timer_text, text="")


# -------------------------------- TIMER START -------------------------------- #
def start_timer():
    global is_running, time_remaining_sec
    if is_running:
        pause_timer()
    else:
        is_running = True
        count_down()


# -------------------------------- GET TIME AFTER RESET -------------------------------- #
def get_new_remaining_time(button_pressed):
    if button_pressed == "reset":
        return SHOT_CLOCK_FRONTCOURT
    if button_pressed == "start":
        return SHOT_CLOCK_FULL


# -------------------------------- COUNTDOWN MECHANISM -------------------------------- #
def count_down():
    global time_remaining_sec, is_running, timer

    if is_running:
        time_remaining_sec -= 0.1

        # Extract the integer and fractional parts of the seconds
        integer_seconds = int(time_remaining_sec)
        tenths = int((time_remaining_sec - integer_seconds) * 10)

        # Format the time based on remaining time
        if time_remaining_sec > 5.0:
            time_string = f"{integer_seconds}"
            canvas.itemconfig(timer_text, font=INTEGER_FONT)
        else:
            time_string = f"{integer_seconds}.{tenths}"
            canvas.itemconfig(timer_text, font=DECIMAL_FONT)

        canvas.itemconfig(timer_text, text=time_string)

        if time_remaining_sec <= 0:
            play_sound()
            is_running = False
            canvas.itemconfig(timer_text, text="0.0")

    if is_running:
        timer = window.after(100, count_down)


# -------------------------------- UI SETUP -------------------------------- #
window = Tk()
window.title("Heittokello")
window.config(padx=100, pady=50, bg=YELLOW)
window.geometry("1000x900")
title_label = Label(text="Heittokello", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 72, "bold"))
title_label.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
# catz_img = PhotoImage(file="catz.png")
# canvas.create_image(100, 112, image=catz_img)
timer_text = canvas.create_text(100, 130, text="0.0", fill="red", font=(FONT_NAME, 22, "bold"))
canvas.grid(column=1, row=1)

start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2, pady=10)
reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=1, row=2, pady=10)
buzzer_button = Button(text="buzzer", highlightthickness=0, command=play_sound)
buzzer_button.grid(column=0, row=3, pady=10)

window.mainloop()


