
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 15:42:58 2025

@author: sarap
"""

from graphics import * 
import tkinter as tk
import webbrowser
import csv
import os

# Put the window in the center of the screen
def center_window(win, width, height):
    root = tk.Tk()
    root.withdraw()
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    root.destroy()
    x = (screen_w - width) // 2
    y = (screen_h - height) // 2
    win.master.geometry(f"{width}x{height}+{x}+{y}")

# Get user input from a box (optionally for passwords)
def get_input_in_box(win, box, is_password=False):
    text = ""
    display = Text(box.getCenter(), "")
    display.setSize(16)
    display.setTextColor("black")
    display.draw(win)

    while True:
        key = win.getKey()
        if key == "Return":
            break
        elif key == "BackSpace":
            text = text[:-1]
        elif len(key) == 1:
            text += key
        if is_password:
            display.setText("*" * len(text))
        else:
            display.setText(text)

    return text

# Draw input box and label
def draw_input_box(win, x, y, label):
    label_text = Text(Point(x, y + 60), label)
    label_text.setSize(16)
    label_text.setTextColor("black")
    label_text.draw(win)

    box = Rectangle(Point(x - 140, y), Point(x + 140, y + 50))
    box.setFill("white")
    box.draw(win)

    return box

# Check if mouse click is inside a rectangle
def inside(click, rect):
    return rect.getP1().getX() <= click.getX() <= rect.getP2().getX() and \
           rect.getP1().getY() <= click.getY() <= rect.getP2().getY()

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
        fieldnames = ["username", "password", "verification", "vehicle", "identity" ]
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
            found = False
            for username, data in users.items():
                if data["verification"] == code:
                    win.close()
                    blank_page(username)
                    found = True
                    break
            if not found:
                msg.setText("Incorrect code or no associated account.")

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
    login_text = Text(login_btn.getCenter(), "Log In")
    login_text.setTextColor("white")
    login_text.setSize(14)
    login_text.draw(win)

    forgot_btn = Rectangle(Point(100, 170), Point(300, 210))
    forgot_btn.setFill("#8e6f3e")
    forgot_btn.draw(win)
    forgot_text = Text(forgot_btn.getCenter(), "Forgot Login")
    forgot_text.setTextColor("white")
    forgot_text.setSize(14)
    forgot_text.draw(win)

    back_btn = Rectangle(Point(100, 100), Point(300, 150))
    back_btn.setFill("#555960")
    back_btn.draw(win)
    back_text = Text(back_btn.getCenter(), "Back")
    back_text.setTextColor("white")
    back_text.setSize(14)
    back_text.draw(win)

    error = Text(Point(200, 310), "")
    error.setSize(14)
    error.setTextColor("red")
    error.draw(win)

    username = ""
    password = ""

    while True:
        click = win.getMouse()
        if inside(click, username_box):
            username = get_input_in_box(win, username_box)
        elif inside(click, password_box):
            password = get_input_in_box(win, password_box, True)
        elif inside(click, login_btn):
            users = load_users()
            if username in users and users[username]["password"] == password:
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
   
    identity_label = Text(Point(x, 260), "Select Identity:")
    identity_label.setSize(14)
    identity_label.draw(win)
    
    student_btn = Rectangle(Point(100, 220), Point(190, 250))
    student_btn.setFill("#fbbc05")
    student_btn.draw(win)
    Text(student_btn.getCenter(), "Student").draw(win)
    
    teacher_btn = Rectangle(Point(210, 220), Point(300, 250))
    teacher_btn.setFill("#fbbc05")
    teacher_btn.draw(win)
    Text(teacher_btn.getCenter(), "Teacher").draw(win)
    
    selected_identity = ""  
        

    signup_btn = Rectangle(Point(100, 150), Point(300, 200))
    signup_btn.setFill("#daaa00")
    signup_btn.draw(win)
    signup_text = Text(signup_btn.getCenter(), "Create Account")
    signup_text.setTextColor("white")
    signup_text.setSize(14)
    signup_text.draw(win)

    back_btn = Rectangle(Point(100, 90), Point(300, 140))
    back_btn.setFill("#555960")
    back_btn.draw(win)
    back_text = Text(back_btn.getCenter(), "Back")
    back_text.setTextColor("white")
    back_text.setSize(14)
    back_text.draw(win)

    error = Text(Point(200, 50), "")
    error.setSize(14)
    error.setTextColor("red")
    error.draw(win)

    username = ""
    password = ""
    verification = ""
    vehicle = ""
    retry_btn = None
    retry_text = None

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
        elif inside(click, signup_btn):
            if username and password and verification and vehicle and selected_identity:
                if username and password and verification and vehicle and selected_identity:
                    result = save_user_to_csv(username, password, verification, vehicle, selected_identity)
                    if result == "success":
                        win.close()
                        blank_page(username)
                        break
                    elif result == "duplicate_username":
                        error.setText("Username already exists.")
                elif result == "duplicate_credentials":
                    error.setText("This exact account already exists.")
            else:
                error.setText("All fields are required.")
                if retry_btn:
                    retry_btn.undraw()
                    retry_text.undraw()
                retry_btn = Rectangle(Point(100, 130), Point(300, 170))
                retry_btn.setFill("#f4b400")
                retry_btn.draw(win)
                retry_text = Text(retry_btn.getCenter(), "Retry")
                retry_text.setTextColor("white")
                retry_text.setSize(14)
                retry_text.draw(win)
        elif inside(click, back_btn):
            win.close()
            main()
            break
        elif retry_btn and inside(click, retry_btn):
            error.setText("")
            retry_btn.undraw()
            retry_text.undraw()
            username = password = verification = vehicle = ""
            username_box = draw_input_box(win, x, 600, "Username:")
            password_box = draw_input_box(win, x, 500, "Password:")
            verification_box = draw_input_box(win, x, 400, "Set Verification Code:")
            vehicle_box = draw_input_box(win, x, 300, "Vehicle Number:")
        elif inside(click, student_btn):
            selected_identity = "Student"
            student_btn.setFill("green")
            teacher_btn.setFill("#fbbc05")
        elif inside(click, teacher_btn):
            selected_identity = "Teacher"
            teacher_btn.setFill("green")
            student_btn.setFill("#fbbc05")
            


# Save all users to file
def save_all_users(users):
    with open("users.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["username", "password", "verification", "vehicle", "identity"])
        writer.writeheader()
        for user in users.values():
            writer.writerow(user)

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
            old_username = user["username"]
        elif inside(click, back_btn):
            win.close()
            blank_page(user["username"])
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

    map_btn = Rectangle(Point(100, 150), Point(500, 200))
    map_btn.setFill("#0f9d58")
    map_btn.draw(win)
    Text(map_btn.getCenter(), "Google Map").draw(win)

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
        elif inside(click, map_btn):
            win.close()
            show_blank_window("Google Map", username)
            break
        elif inside(click, edit_btn):
            win.close()
            edit_account_info(username)
            break

# Shows empty screen for other sections
def show_blank_window(title, username):
    win = GraphWin(title, 600, 600)
    center_window(win, 600, 600)
    win.setBackground("#cfb991")

    Text(Point(300, 570), f"{title} Content Goes Here").draw(win)

    # Add "View Permit Site" button if on Parking Policy page
    if title == "Parking Policy":
        permit_btn = Rectangle(Point(200, 520), Point(400, 560))
        permit_btn.setFill("#1a73e8")
        permit_btn.draw(win)
        Text(permit_btn.getCenter(), "View Permit Site").draw(win)
 
        permit_info = [
            "Student Permits",
            "1. “C” Permit - $100/year - C lots on campus edges",
            "2. Student Garage Permit - includes garage + C lots",
            "",
            "Faculty & Staff Permits",
            "1. “A” Permit - $250/year - A, AB, ABC lots",
            "2. “B” Permit - $100/year - AB, ABC lots",
            "3. “ID” Permit - $20/year - limited hours in A/AB/ABC",
            "4. Reserved Permit - $1000/year - reserved spaces"
            ]   
        y = 300
        for line in permit_info:
            text = Text(Point(300, y), line)
            text.setSize(10)
            text.draw(win)
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

# Main menu screen
def main():
    win = GraphWin("Welcome", 400, 500)
    center_window(win, 400, 500)
    win.setCoords(0, 0, 400, 500)
    win.setBackground("#ffe0b2")

    Text(Point(200, 420), "Welcome to BoilerParking!").draw(win)

    login_btn = Rectangle(Point(100, 300), Point(300, 350))
    login_btn.setFill("#daaa00")
    login_btn.draw(win)
    Text(login_btn.getCenter(), "Login").draw(win)

    signup_btn = Rectangle(Point(100, 200), Point(300, 250))
    signup_btn.setFill("#0f9d58")
    signup_btn.draw(win)
    Text(signup_btn.getCenter(), "Sign Up").draw(win) 
    
    logo = Image(Point(200, 100), "/Users/tiankean/Downloads/purduepark.gif")
    logo.draw(win)

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

# Start the program
if __name__ == "__main__":
    main()
