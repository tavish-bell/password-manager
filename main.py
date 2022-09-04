"""
password manager
"""

import json
import tkinter
from random import choice, randint, shuffle
from tkinter import *
from tkinter import messagebox

import pyperclip


# -------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    """
    generate secure password using letters, 
    numbers, and symbols
    """
    letters = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
    ]
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    symbols = ["!", "#", "$", "%", "&", "(", ")", "*", "+"]

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols

    shuffle(password_list)
    password = "".join(password_list)

    # populate password field with generated password
    password_entry.insert(0, password)

    # copy generated password to clipboard
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    """
    update password manager txt file with user input website
    and password information
    """
    website = website_entry.get()
    email = email_username_entry.get()
    password = password_entry.get()
    new_data = {website: {"email": email, "password": password}}

    if len(website) == 0 or len(password) == 0:

        messagebox.showerror(
            title="Error", message="Please don't leave any fields empty"
        )
    else:
        try:
            # opening file
            with open("data.json", "r") as data_file:
                # reading old data inside
                data = json.load(data_file)

        except FileNotFoundError:
            # create new file
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)

        else:
            # update old data with new data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                # save updated data
                json.dump(data, data_file, indent=4)

        finally:
            # confirm success to user
            messagebox.showinfo(title="Success", message="Your password has been saved")

            # clear entry fields
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# --------------------- FIND PASSWORD  ----------------------------------#


def find_password():
    """
    search password database to find username and password for website
    """
    website = website_entry.get()

    try:
        with open("data.json", "r") as data_file:
            # reading old data inside
            data = json.load(data_file)

    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No datafile found")

    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            new_data = {website: {"email": email, "password": password}}
            # put this info into a pop-up
            messagebox.showinfo(
                title=website, message=f"Email: {email}\nPassword: {password}",
            )
        else:
            messagebox.showinfo(
                title="Error", message="You haven't created a login for this site yet!"
            )


# ---------------------------- UI SETUP ------------------------------- #
# create window
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# create canvas / display logo
logo_image = PhotoImage(file="logo.png")
canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=1, row=0)

# labels
website_label = tkinter.Label(text="Website:")
website_label.grid(column=0, row=1)
email_username_label = tkinter.Label(text="Email/Username:")
email_username_label.grid(column=0, row=2)
password_label = tkinter.Label(text="Password:")
password_label.grid(column=0, row=3)

# entries
website_entry = tkinter.Entry(width=35)
website_entry.grid(column=1, row=1, columnspan=2)
# have cusor start in website entry box
website_entry.focus()
email_username_entry = tkinter.Entry(width=35)
email_username_entry.grid(column=1, row=2, columnspan=2)
# pre-populate field
email_username_entry.insert(0, "tavishjbell@gmail.com")
password_entry = tkinter.Entry(width=35)
password_entry.grid(column=1, row=3, columnspan=2)

# buttons
generate_button = tkinter.Button(text="Generate", width=7, command=generate_password)
generate_button.grid(column=2, row=3)
add_button = tkinter.Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)
search_button = tkinter.Button(text="Search", width=7, command=find_password)
search_button.grid(column=2, row=1)

window.mainloop()
