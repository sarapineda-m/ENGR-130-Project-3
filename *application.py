# ===============================
# BoilerParking GUI - Notes & Tips
# ===============================

# - This code is beginner-friendly and not fully optimized.
# - Some windows (especially Grant Street Garage) take time to load.
# - Input boxes may require multiple clicks before typing is detected.
# - You must press "Enter" after typing in each input box.
# - Sometimes pressing Enter more than once is needed.
# - If you already hit Enter and try to retype, your new text will appear under the old one.
# - Some buttons may need to be clicked more than once to register.
# - When creating an account, there is no confirmation message.
# - You must go back to the login screen and try logging in to check if it worked.
#
# **We asked ChatGPT to help us understand how to connect the sensor (micro:bit) to the Spyder Python GUI**

from graphics import *  # for GUI drawing
import tkinter as tk    # for centering windows
import webbrowser       # to open URLs
import csv              # to read/write user data
import os               # to check if file exists
import datetime         # to log time
import random           # to show fake parking spots
import serial
import serial.tools.list_ports


ports = serial.tools.list_ports.comports()
for port in ports:
    print(port.device, port.description)

def read_sensor_status():
    try:
        ser = serial.Serial("COM5", 115200, timeout=1)  # Use your confirmed port
        line = ser.readline().decode().strip()
        ser.close()
        if line in ["O", "L", "R", "X"]:
            return line
        return "O"
    except:
        return "O"


# makes window show in center of screen
def center_window(win, width, height):
    root = tk.Tk()
    root.withdraw()
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    root.destroy()
    x = (screen_w - width) // 2
    y = (screen_h - height) // 2
    win.master.geometry(f"{width}x{height}+{x}+{y}")

# checks if user clicked inside a box
def inside(p, box):
    x1 = box.getP1().getX()
    y1 = box.getP1().getY()
    x2 = box.getP2().getX()
    y2 = box.getP2().getY()
    return x1 <= p.getX() <= x2 and y1 <= p.getY() <= y2

# draw a text label and box for input
def draw_input_box(win, x, y, label):
    Text(Point(x, y + 60), label).draw(win)
    box = Rectangle(Point(x - 140, y), Point(x + 140, y + 50))
    box.setFill("white")
    box.draw(win)
    return box

# get what user types in input box
def get_input_in_box(win, box, is_password=False):
    text = ""
    display = Text(box.getCenter(), "")
    display.setSize(16)
    display.setTextColor("black")
    display.draw(win)

    while True:
        click = win.getMouse()
        if inside(click, box):
            break

    display.setText("")

    while True:
        key = win.getKey()
        if key == "Return":
            break
        elif key == "BackSpace":
            text = text[:-1]
        elif len(key) == 1:
            text += key
        display.setText("*" * len(text) if is_password else text)

    return text

# save new user to csv file
def save_user_to_csv(username, password, verification, vehicle, classification):
    users = load_users()
    for user in users.values():
        if user["username"] == username:
            return "duplicate_username"
        if (user["password"] == password and user["verification"] == verification
            and user["vehicle"] == vehicle):
            return "duplicate_credentials"
    file_exists = os.path.exists("users.csv")
    with open("users.csv", "a", newline="") as file:
        fieldnames = ["username", "password", "verification", "vehicle", "classification"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "username": username,
            "password": password,
            "verification": verification,
            "vehicle": vehicle,
            "classification": classification
        })
    return "success"

# load all users from file
def load_users():
    users = {}
    if os.path.exists("users.csv"):
        with open("users.csv", "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                users[row["username"]] = row
    return users

# save everyone to file
def save_all_users(users):
    with open("users.csv", "w", newline="") as file:
        fieldnames = ["username", "password", "verification", "vehicle", "classification"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for user in users.values():
            writer.writerow(user)

# log what the user did (login, signup, etc.)
def log_account_activity(username, action):
    users = load_users()
    if username not in users:
        return
    user = users[username]
    file_path = "account_activity.csv"
    file_exists = os.path.exists(file_path)
    with open(file_path, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["username", "action", "timestamp", "password", "verification", "vehicle", "classification"])
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([username, action, timestamp, user["password"], user["verification"], user["vehicle"], user["classification"]])

# signup screen
def signup_page():
    win = GraphWin("Sign Up", 400, 800)
    center_window(win, 400, 800)
    win.setCoords(0, 0, 400, 800)
    win.setBackground("#cfb991")
    x = 200
    u_box = draw_input_box(win, x, 600, "Username:")
    p_box = draw_input_box(win, x, 500, "Password:")
    v_box = draw_input_box(win, x, 400, "Verification Code:")
    veh_box = draw_input_box(win, x, 300, "Vehicle Number:")
    c_box = draw_input_box(win, x, 220, "Classification:")
    signup = Rectangle(Point(100, 150), Point(300, 200))
    signup.setFill("#daaa00")
    signup.draw(win)
    Text(signup.getCenter(), "Create Account").draw(win)
    back = Rectangle(Point(100, 90), Point(300, 140))
    back.setFill("#555960")
    back.draw(win)
    Text(back.getCenter(), "Back").draw(win)
    msg = Text(Point(200, 50), "")
    msg.setTextColor("red")
    msg.draw(win)

    while True:
        click = win.getMouse()
        if inside(click, u_box):
            u = get_input_in_box(win, u_box)
        elif inside(click, p_box):
            p = get_input_in_box(win, p_box)
        elif inside(click, v_box):
            v = get_input_in_box(win, v_box)
        elif inside(click, veh_box):
            ve = get_input_in_box(win, veh_box)
        elif inside(click, c_box):
            c = get_input_in_box(win, c_box)
        elif inside(click, signup):
            if u and p and v and ve and c:
                result = save_user_to_csv(u, p, v, ve, c)
                if result == "success":
                    log_account_activity(u, "signup")
                    win.close()
                    blank_page(u)
                    break
                elif result == "duplicate_username":
                    msg.setText("Username taken.")
                elif result == "duplicate_credentials":
                    msg.setText("Account exists.")
            else:
                msg.setText("Fill all fields.")
        elif inside(click, back):
            win.close()
            main()
            break

# login screen
def login_page():
    win = GraphWin("Login", 400, 700)
    center_window(win, 400, 700)
    win.setCoords(0, 0, 400, 700)
    win.setBackground("#cfb991")
    x = 200
    u_box = draw_input_box(win, x, 450, "Username:")
    p_box = draw_input_box(win, x, 350, "Password:")
    login = Rectangle(Point(100, 230), Point(300, 280))
    login.setFill("#daaa00")
    login.draw(win)
    Text(login.getCenter(), "Log In").draw(win)
    forgot = Rectangle(Point(100, 170), Point(300, 210))
    forgot.setFill("#8e6f3e")
    forgot.draw(win)
    Text(forgot.getCenter(), "Forgot Login").draw(win)
    back = Rectangle(Point(100, 100), Point(300, 150))
    back.setFill("#555960")
    back.draw(win)
    Text(back.getCenter(), "Back").draw(win)
    msg = Text(Point(200, 310), "")
    msg.setTextColor("red")
    msg.draw(win)

    while True:
        click = win.getMouse()
        if inside(click, u_box):
            u = get_input_in_box(win, u_box)
        elif inside(click, p_box):
            p = get_input_in_box(win, p_box, True)
        elif inside(click, login):
            users = load_users()
            if u in users and users[u]["password"] == p:
                log_account_activity(u, "login")
                win.close()
                blank_page(u)
                break
            else:
                msg.setText("Wrong username or password.")
        elif inside(click, forgot):
            win.close()
            forgot_login_page()
            break
        elif inside(click, back):
            win.close()
            main()
            break

# forgot username/password screen
def forgot_login_page():
    win = GraphWin("Forgot Login", 400, 300)
    center_window(win, 400, 300)
    win.setCoords(0, 0, 400, 300)
    win.setBackground("#cfb991")
    box = draw_input_box(win, 200, 180, "Enter Verification Code:")
    submit = Rectangle(Point(100, 90), Point(300, 140))
    submit.setFill("#daaa00")
    submit.draw(win)
    Text(submit.getCenter(), "Submit").draw(win)
    msg = Text(Point(200, 50), "")
    msg.setTextColor("red")
    msg.draw(win)

    while True:
        click = win.getMouse()
        if inside(click, box):
            code = get_input_in_box(win, box)
        elif inside(click, submit):
            users = load_users()
            for name, info in users.items():
                if info["verification"] == code:
                    win.close()
                    blank_page(name)
                    return
            msg.setText("Invalid code.")

# dashboard (after login/signup)
def blank_page(username):
    win = GraphWin("Dashboard", 600, 400)
    center_window(win, 600, 400)
    win.setBackground("#cfb991")
    policy = Rectangle(Point(100, 250), Point(500, 300))
    policy.setFill("#4285f4")
    policy.draw(win)
    Text(policy.getCenter(), "Parking Policy").draw(win)
    nav = Rectangle(Point(100, 150), Point(500, 200))
    nav.setFill("#0f9d58")
    nav.draw(win)
    Text(nav.getCenter(), "Navigation").draw(win)
    edit = Rectangle(Point(100, 50), Point(500, 100))
    edit.setFill("#fbbc05")
    edit.draw(win)
    Text(edit.getCenter(), "Edit Account Info").draw(win)

    while True:
        click = win.getMouse()
        if inside(click, policy):
            win.close()
            show_blank_window("Parking Policy", username)
            break
        elif inside(click, nav):
            win.close()
            show_navigation_window(username)
            break
        elif inside(click, edit):
            win.close()
            edit_account_info(username)
            break

# screen to edit account info
def edit_account_info(username):
    users = load_users()
    if username not in users:
        return
    user = users[username]
    old_username = username

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

# shows a list of garages with buttons
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

# shows garage info when clicked
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

    if garage_name == "Grant Street Garage":
        sensor_status = read_sensor_status()


        # Begin with 50 spots
        available = 50

        if sensor_status == "X":
            available -= 2
        elif sensor_status in ["L", "R"]:
            available -= 1
        # If "O", don't subtract

        Text(Point(250, 150), "Available Spots: " + str(available)).draw(win)
        Text(Point(250, 200), "Permits Allowed: " + garage_info[garage_name]).draw(win)
    elif garage_name in garage_info:
        permits = garage_info[garage_name]
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


# shows parking policy info or other blank pages
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

# welcome screen
def main():
    win = GraphWin("Welcome", 400, 500)
    center_window(win, 400, 500)
    win.setCoords(0, 0, 400, 500)
    win.setBackground("#cfb991")

    # try to load Purdue gif, otherwise show text
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

# run the app
if __name__ == "__main__":
    main()
