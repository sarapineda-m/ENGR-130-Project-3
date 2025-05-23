# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 19:06:00 2025

@author: sarap
"""
from graphics import * 
import tkinter as tk
import webbrowser
import csv
import os
import datetime
import random


def log_account_activity(username, action):
    """Logs full account info + activity into account_activity.csv."""
    users = load_users()
    if username not in users:
        return  # just in case

    user = users[username]
    file_path = "account_activity.csv"
    file_exists = os.path.exists(file_path)

    with open(file_path, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["username", "action", "timestamp", "password", "verification", "vehicle", "classification"])
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([
            username,
            action,
            timestamp,
            user["password"],
            user["verification"],
            user["vehicle"],
            user["identity"]  # or change to 'role' or 'classification' if renamed
        ])


from graphics import *
import tkinter as tk
import csv
import os
import datetime
import random
import webbrowser

# center the graphics window
def center_window(win, w, h):
    root = tk.Tk()
    root.withdraw()
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    root.destroy()
    x = (sw - w) // 2
    y = (sh - h) // 2
    win.master.geometry(str(w) + "x" + str(h) + "+" + str(x) + "+" + str(y))

# check if click is in box
def inside(p, box):
    x1 = box.getP1().getX()
    y1 = box.getP1().getY()
    x2 = box.getP2().getX()
    y2 = box.getP2().getY()
    return x1 <= p.getX() <= x2 and y1 <= p.getY() <= y2

# draw label and input box
def draw_input_box(win, x, y, label):
    Text(Point(x, y + 60), label).draw(win)
    box = Rectangle(Point(x - 140, y), Point(x + 140, y + 50))
    box.setFill("white")
    box.draw(win)
    return box

# get typed input
def get_input_in_box(win, box, is_pass=False):
    user_text = ""
    output = Text(box.getCenter(), "")
    output.setSize(16)
    output.draw(win)

    while True:
        click = win.getMouse()
        if inside(click, box):
            break

    output.setText("")

    while True:
        key = win.getKey()
        if key == "Return":
            break
        elif key == "BackSpace":
            user_text = user_text[:-1]
        elif len(key) == 1:
            user_text += key
        output.setText("*" * len(user_text) if is_pass else user_text)

    return user_text

# Load users from file
def load_users():
    users = {}
    if os.path.exists("users.csv"):
        with open("users.csv", "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                users[row["username"]] = row
    return users

# Save new user to file
def save_user_to_csv(username, password, verification, vehicle, identity):
    users = load_users()
    for user in users.values():
        if (user["username"] == username and user["password"] == password and
            user["verification"] == verification and user["vehicle"] == vehicle):
            return "duplicate_credentials"
        elif user["username"] == username:
            return "duplicate_username"
    file_exists = os.path.isfile("users.csv")
    with open("users.csv", "a", newline="") as file:
        fieldnames = ["username", "password", "verification", "vehicle", "identity"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "username": username,
            "password": password,
            "verification": verification,
            "vehicle": vehicle,
            "identity": identity
        })
    return "success"

# Save all users to file
def save_all_users(users):
    with open("users.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["username", "password", "verification", "vehicle", "identity"])
        writer.writeheader()
        for user in users.values():
            writer.writerow(user)

# Forgot verification login logic
def forgot_login_page():
    win = GraphWin("Forgot Login", 400, 300)
    center_window(win, 400, 300)
    win.setCoords(0, 0, 400, 300)
    win.setBackground("#cfb991")
    code_box = draw_input_box(win, 200, 180, "Enter Verification Code:")
    submit_btn = Rectangle(Point(100, 90), Point(300, 140))
    submit_btn.setFill("#daaa00")
    submit_btn.draw(win)
    Text(submit_btn.getCenter(), "Submit").draw(win)
    msg = Text(Point(200, 50), "")
    msg.setSize(14)
    msg.setTextColor("red")
    msg.draw(win)
    while True:
        click = win.getMouse()
        if inside(click, code_box):
            code = get_input_in_box(win, code_box)
        elif inside(click, submit_btn):
            users = load_users()
            for username, data in users.items():
                if data["verification"] == code:
                    win.close()
                    blank_page(username)
                    return
            msg.setText("Incorrect code or no associated account.")

# Signup screen
def signup_page():
    win = GraphWin("Sign Up", 400, 800)
    center_window(win, 400, 800)
    win.setCoords(0, 0, 400, 800)
    win.setBackground("#cfb991")

    x = 200
    username_box = draw_input_box(win, x, 600, "Username:")
    password_box = draw_input_box(win, x, 500, "Password:")
    verification_box = draw_input_box(win, x, 400, "Set Verification Code:")
    vehicle_box = draw_input_box(win, x, 300, "Vehicle Number:")
    identity_box = draw_input_box(win, x, 220, "Classification:")
    signup_btn = Rectangle(Point(100, 150), Point(300, 200))
    signup_btn.setFill("#daaa00")
    signup_btn.draw(win)
    Text(signup_btn.getCenter(), "Create Account").draw(win)
    back_btn = Rectangle(Point(100, 90), Point(300, 140))
    back_btn.setFill("#555960")
    back_btn.draw(win)
    Text(back_btn.getCenter(), "Back").draw(win)
    error = Text(Point(200, 50), "")
    error.setSize(14)
    error.setTextColor("red")
    error.draw(win)
    while True:
        click = win.getMouse()
        if inside(click, username_box):
            username = get_input_in_box(win, username_box)
        elif inside(click, password_box):
            password = get_input_in_box(win, password_box)
        elif inside(click, verification_box):
            verification = get_input_in_box(win, verification_box)
        elif inside(click, vehicle_box):
            vehicle = get_input_in_box(win, vehicle_box)
        elif inside(click, identity_box):
            selected_identity = get_input_in_box(win, identity_box)
        elif inside(click, signup_btn):
            if username and password and verification and vehicle and selected_identity:
                result = save_user_to_csv(username, password, verification, vehicle, selected_identity)
                if result == "success":
                    log_account_activity(username, "signup")  # <--- Add this line
                    win.close()
                    blank_page(username)
                    break
                elif result == "duplicate_username":
                    error.setText("Username already exists.")
                elif result == "duplicate_credentials":
                    error.setText("This exact account already exists.")
            else:
                error.setText("All fields are required.")
        elif inside(click, back_btn):
            win.close()
            main()
            break

# Login screen
def login_page():
    win = GraphWin("Login", 400, 700)
    center_window(win, 400, 700)
    win.setCoords(0, 0, 400, 700)
    win.setBackground("#cfb991")

    x = 200
    username_box = draw_input_box(win, x, 450, "Username:")
    password_box = draw_input_box(win, x, 350, "Password:")
    login_btn = Rectangle(Point(100, 230), Point(300, 280))
    login_btn.setFill("#daaa00")
    login_btn.draw(win)
    Text(login_btn.getCenter(), "Log In").draw(win)
    forgot_btn = Rectangle(Point(100, 170), Point(300, 210))
    forgot_btn.setFill("#8e6f3e")
    forgot_btn.draw(win)
    Text(forgot_btn.getCenter(), "Forgot Login").draw(win)
    back_btn = Rectangle(Point(100, 100), Point(300, 150))
    back_btn.setFill("#555960")
    back_btn.draw(win)
    Text(back_btn.getCenter(), "Back").draw(win)
    error = Text(Point(200, 310), "")
    error.setSize(14)
    error.setTextColor("red")
    error.draw(win)
    while True:
        click = win.getMouse()
        if inside(click, username_box):
            username = get_input_in_box(win, username_box)
        elif inside(click, password_box):
            password = get_input_in_box(win, password_box, True)
        elif inside(click, login_btn):
            users = load_users()
            if username in users and users[username]["password"] == password:
                log_account_activity(username, "login")  # <--- Add this line
                win.close()
                blank_page(username)
                break
            else:
                error.setText("Invalid username or password.")
        elif inside(click, forgot_btn):
            win.close()
            forgot_login_page()
            break
        elif inside(click, back_btn):
            win.close()
            main()
            break
        
# Edit account info
def edit_account_info(username):
    users = load_users()
    if username not in users:
        return
    old_username = username
    user = users[username]

    win = GraphWin("Edit Info", 450, 700)
    center_window(win, 450, 700)
    win.setCoords(0, 0, 450, 700)
    win.setBackground("#cfb991")
    x = 225

    def draw_field(y, label, value):
        Text(Point(x, y + 60), label).draw(win)
        box = Rectangle(Point(x - 140, y), Point(x + 140, y + 50))
        box.setFill("white")
        box.draw(win)
        text = Text(box.getCenter(), value)
        text.draw(win)
        return box, text

    user_box, user_text = draw_field(540, "Username:", user["username"])
    pass_box, pass_text = draw_field(430, "Password:", user["password"])
    vehicle_box, vehicle_text = draw_field(320, "Vehicle Number:", user["vehicle"])
    verify_box, verify_text = draw_field(210, "Verification Code:", user["verification"])

    update_btn = Rectangle(Point(100, 150), Point(350, 190))
    update_btn.setFill("#0f9d58")
    update_btn.draw(win)
    Text(update_btn.getCenter(), "Update Info").draw(win)

    back_btn = Rectangle(Point(100, 80), Point(350, 130))
    back_btn.setFill("#555960")
    back_btn.draw(win)
    Text(back_btn.getCenter(), "Back").draw(win)

    while True:
        click = win.getMouse()
        if inside(click, user_box):
            user_text.setText("")
            new_user = get_input_in_box(win, user_box)
            if new_user and new_user not in users:
                user["username"] = new_user
                user_text.setText(new_user)
            else:
                user_text.setText(user["username"])
        elif inside(click, pass_box):
            pass_text.setText("")
            new_pass = get_input_in_box(win, pass_box)
            if new_pass:
                user["password"] = new_pass
                pass_text.setText(new_pass)
        elif inside(click, vehicle_box):
            vehicle_text.setText("")
            new_vehicle = get_input_in_box(win, vehicle_box)
            if new_vehicle:
                user["vehicle"] = new_vehicle
                vehicle_text.setText(new_vehicle)
        elif inside(click, verify_box):
            verify_text.setText("")
            new_verify = get_input_in_box(win, verify_box)
            if new_verify:
                user["verification"] = new_verify
                verify_text.setText(new_verify)
        elif inside(click, update_btn):
            if old_username != user["username"]:
                del users[old_username]
            users[user["username"]] = user
            save_all_users(users)
            log_account_activity(user["username"], "updated info")  
            old_username = user["username"]

        elif inside(click, back_btn):
            win.close()
            blank_page(user["username"])
            break

def show_navigation_window(username):
    win = GraphWin("Garage Navigation", 600, 600)
    center_window(win, 600, 600)
    win.setBackground("#cfb991")

    garages = [
        ("Grant Street Garage", 100),
        ("University Street Garage", 180),
        ("Wood Street Garage", 260),
        ("Harrison Street Garage", 340),
        ("McCutcheon Garage", 420)
    ]

    buttons = []
    for name, y in garages:
        btn = Rectangle(Point(100, y), Point(500, y + 40))
        btn.setFill("#0f9d58")
        btn.draw(win)
        Text(btn.getCenter(), name).draw(win)
        buttons.append((btn, name))

    # Back button
    back_btn = Rectangle(Point(200, 500), Point(400, 550))
    back_btn.setFill("#555960")
    back_btn.draw(win)
    Text(back_btn.getCenter(), "Back").draw(win)

    while True:
        click = win.getMouse()
        if inside(click, back_btn):
            win.close()
            blank_page(username)
            break
        for btn, name in buttons:
            if inside(click, btn):
                win.close()
                show_garage_info_window(username, name)
                return

def show_garage_info_window(user, garage_name):
    win = GraphWin(garage_name, 500, 400)
    center_window(win, 500, 400)
    win.setBackground("#cfb991")

    title = Text(Point(250, 50), garage_name)
    title.setSize(20)
    title.draw(win)

    garage_info = {
        "Grant Street Garage": "C, A, Staff",
        "University Street Garage": "C, A",
        "Wood Street Garage": "C only",
        "Harrison Street Garage": "C, Staff",
        "McCutcheon Garage": "All permits"
    }

    if garage_name in garage_info:
        if garage_name in garage_info:
            permits = garage_info[garage_name]
        else:
            permits = "Unknown"
        spots = random.randint(15, 70)
        Text(Point(250, 150), "Available Spots: " + str(spots)).draw(win)
        Text(Point(250, 200), "Permits Allowed: " + permits).draw(win)
    else:
        Text(Point(250, 150), "No data found").draw(win)

    back_btn = Rectangle(Point(150, 300), Point(350, 350))
    back_btn.setFill("#555960")
    back_btn.draw(win)
    Text(back_btn.getCenter(), "Back").draw(win)

    while True:
        click = win.getMouse()
        if inside(click, back_btn):
            win.close()
            show_navigation_window(user)
            break


# Blank dashboard
def blank_page(username):
    win = GraphWin("Dashboard", 600, 400)
    center_window(win, 600, 400)
    win.setBackground("#cfb991")
    policy_btn = Rectangle(Point(100, 250), Point(500, 300))
    policy_btn.setFill("#4285f4")
    policy_btn.draw(win)
    Text(policy_btn.getCenter(), "Parking Policy").draw(win)
    nav_btn = Rectangle(Point(100, 150), Point(500, 200))
    nav_btn.setFill("#0f9d58")
    nav_btn.draw(win)
    Text(nav_btn.getCenter(), "Navigation").draw(win)
    edit_btn = Rectangle(Point(100, 50), Point(500, 100))
    edit_btn.setFill("#fbbc05")
    edit_btn.draw(win)
    Text(edit_btn.getCenter(), "Edit Account Info").draw(win)
    while True:
        click = win.getMouse()
        if inside(click, policy_btn):
            win.close()
            show_blank_window("Parking Policy", username)
            break
        elif inside(click, nav_btn):
            win.close()
            show_navigation_window(username)
        elif inside(click, edit_btn):
            win.close()
            edit_account_info(username)
            break

# Empty placeholder screen
def show_blank_window(title, username):
    win = GraphWin(title, 600, 600)
    center_window(win, 600, 600)
    win.setBackground("#cfb991")
    Text(Point(300, 570), f"{title} Content Goes Here").draw(win)
    if title == "Parking Policy":
        permit_btn = Rectangle(Point(200, 520), Point(400, 560))
        permit_btn.setFill("#1a73e8")
        permit_btn.draw(win)
        Text(permit_btn.getCenter(), "View Permit Site").draw(win)
        permit_info = [
            "Student Permits",
            "1. \u201cC\u201d Permit - $100/year - C lots on campus edges",
            "2. Student Garage Permit - includes garage + C lots",
            "",
            "Faculty & Staff Permits",
            "1. \u201cA\u201d Permit - $250/year - A, AB, ABC lots",
            "2. \u201cB\u201d Permit - $100/year - AB, ABC lots",
            "3. \u201cID\u201d Permit - $20/year - limited hours in A/AB/ABC",
            "4. Reserved Permit - $1000/year - reserved spaces"
        ]
        y = 300
        for line in permit_info:
            Text(Point(300, y), line).draw(win)
            y += 20
    back_btn = Rectangle(Point(200, 180), Point(400, 220))
    back_btn.setFill("#555960")
    back_btn.draw(win)
    Text(back_btn.getCenter(), "Back").draw(win)
    while True:
        click = win.getMouse()
        if title == "Parking Policy" and inside(click, permit_btn):
            webbrowser.open("https://purdue.t2hosted.com/Account/Portal")
        elif inside(click, back_btn):
            win.close()
            blank_page(username)
            break

# Main screen
def main():
    win = GraphWin("Welcome", 400, 500)
    center_window(win, 400, 500)
    win.setCoords(0, 0, 400, 500)
    win.setBackground("#cfb991")

    # Purdue GIF logo
    try:
        logo = Image(Point(200, 100), "purduepark.gif")
        logo.draw(win)
    except:
        Text(Point(200, 100), "Logo not found").draw(win)

    Text(Point(200, 200), "Welcome to BoilerParking!").draw(win)

    login_btn = Rectangle(Point(100, 300), Point(300, 350))
    login_btn.setFill("#daaa00")
    login_btn.draw(win)
    Text(login_btn.getCenter(), "Login").draw(win)

    signup_btn = Rectangle(Point(100, 380), Point(300, 430))
    signup_btn.setFill("#0f9d58")
    signup_btn.draw(win)
    Text(signup_btn.getCenter(), "Sign Up").draw(win)

    while True:
        click = win.getMouse()
        if inside(click, login_btn):
            win.close()
            login_page()
            break
        elif inside(click, signup_btn):
            win.close()
            signup_page()
            break

# Run the program
if __name__ == "__main__":
    main()

