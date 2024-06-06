from tkinter import *
from tkinter import messagebox
import pandas as pd
import random
import os
import sys

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

data = pd.read_csv("data/french_words.csv")
to_learn = data.to_dict(orient="records")

try:
    data = pd.read_csv("./word_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
except pd.errors.EmptyDataError:
    is_cancel = messagebox.askokcancel(title="Congrats",message="You have learn all the words.🎉\nDo you want to start again?")
    if is_cancel:
        os.remove("./word_to_learn.csv")
        original_data = pd.read_csv("data/french_words.csv")
        to_learn = original_data.to_dict(orient="records")
    else:
        sys.exit()
else:
    to_learn = data.to_dict(orient="records")




# ------------- Next Card ------------#

def next_card():
    global current_card, flip_timer
    try:
        window.after_cancel(flip_timer)
        current_card = random.choice(to_learn)
        canvas.itemconfig(card_background, image=card_front_image)
        canvas.itemconfig(card_title, text="French", fill='black')
        canvas.itemconfig(card_word, text=current_card["French"], fill='black')
        flip_timer = window.after(3000, func=flip_card)
    except IndexError:
        messagebox.showinfo(message="You have learn all the words.🎉")
        sys.exit()


# ------------- Flip Card -------------- #

def flip_card():
    canvas.itemconfig(card_background, image=card_back_image)
    canvas.itemconfig(card_title, text="English", fill='white')
    canvas.itemconfig(card_word, text=current_card["English"], fill='white')


def is_known():
    to_learn.remove(current_card)
    data = pd.DataFrame(to_learn)
    data.to_csv("word_to_learn.csv", index=False)
    next_card()


# ---------------- UI ------------------- #

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=562)
card_front_image = PhotoImage(file='./images/card_front.png')
card_back_image = PhotoImage(file="./images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_image)
card_title = canvas.create_text(400, 150, text='', font=("Arial", 48, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# --------------- Buttons ---------------- #
cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, command=next_card)
unknown_button.config(highlightthickness=0)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="./images/right.png")
known_button = Button(image=check_image, command=is_known)
known_button.config(highlightthickness=0)
known_button.grid(row=1, column=1)

next_card()

window.mainloop()
