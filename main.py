import tkinter as tk
from tkinter import messagebox, font
import subprocess
import os
import shutil
import datetime
from fontTools.ttLib import TTFont
import webbrowser

# Variables
CONFIG_LOCATION = (
    "C:\\Users\\"
    + os.getlogin()
    + "\\AppData\\Local\\Frontier Developments\\Elite Dangerous\\Options\\"
)
KEYBIND_FOLDER = CONFIG_LOCATION + "Bindings\\"
TRAY_ENABLED = False
DATA_FOLDER = "C:\\Users\\" + os.getlogin() + "\\.KeepMyKeybinds\\"
BACKUP_FOLDER = DATA_FOLDER + "backups\\"
STARTUP_FOLDER = f"C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"



#GUI Init

window = tk.Tk()
ToggleTrayBtn = None
window.title("Keep My Keybinds!")
window.geometry("340x380")
window.iconbitmap("icon.ico")
window.configure(bg="black")



#Config


def get_config():
    try:
        with open(f"{DATA_FOLDER}/config.txt", "r") as f:
            data = f.read()
            data = data.splitlines()
            for i in range(len(data)):
                line = data[i]
                key = line.split("=")[0]
                data = line.split("=")[1]
                match key:
                    case "ServiceEnabled":
                        break
        f.close()
    except FileNotFoundError as e:
        open(f"{DATA_FOLDER}/config.txt", "w").write("ServiceEnabled=False")
    except Exception as e:
        print(e)



#Tray

# def enable_tray():
#     if os.path.exists(os.path.join(os.getcwd(), "KeepMyKeybindsTray.exe")):
#         choice = messagebox.askokcancel("KeepMyKeybinds", "To install the checker, the app will ask for admin permissions this one time. OK to continue?")
#         if not choice:
#             return
#         subprocess.run("keepmykeybindstray.exe install")
#     else:
#         print("noo")
#         choice = messagebox.askokcancel(
#             "KeepMyKeybinds!", "Cannot find tray exe! OK to open the download page?"
#         )
#         if choice:
#             webbrowser.open_new_tab("https://niceygy.net/projects/keepmykeybinds")


# def disable_tray():
#     if is_tray_enabled():
#         shutil.rmtree(os.path.join(STARTUP_FOLDER, "KeepMyKeybindsTray.exe"))
#         messagebox.showinfo(
#             "KepMyKeybinds!",
#             "Tray exe is now disabled. Please restart your device for this to take effect.",
#         )
#         ToggleTrayBtn = tk.Button(
#             text=f"{"Disable" if TRAY_ENABLED else "Enable"} backup checher",
#             fg="#f07b05",
#             bg="black",
#         ).pack(fill="x")
#     else:
#         messagebox.showerror("KeepMyKeybinds!", "Tray exe already disabled.")
#         ToggleTrayBtn = tk.Button(
#             text=f"{"Disable" if TRAY_ENABLED else "Enable"} backup checher",
#             fg="#f07b05",
#             bg="black",
#         ).pack(fill="x")


# def toggle_tray():
#     if is_tray_enabled():
#         disable_tray()
#     else:
#         enable_tray()


# def is_tray_enabled():
#     if os.path.exists(os.path.join(STARTUP_FOLDER, "KeepMyKeybindsTray.exe")):
#         TRAY_ENABLED = True
#         print("Tray enabled")
#         return True
#     else:
#         TRAY_ENABLED = False
#         print("Tray disabled")
#         return False


# get_config()

"""
Cosmetic
"""


# Function to list font families within a font file
def list_font_families(font_path):
    font = TTFont(font_path)
    families = [name.toUnicode() for name in font["name"].names if name.nameID == 1]
    return families


# Function to register a custom font
def register_custom_font(root, font_path):
    font_families = list_font_families(font_path)

    if font_families:
        # Register the first font family
        custom_font_family = font_families[0]
        root.tk.call(
            "font",
            "create",
            custom_font_family,
            "-family",
            custom_font_family,
            "-size",
            12,
        )

        # Set the registered font as default for the application
        default_font = font.Font(family=custom_font_family, size=12)
        root.option_add("*Font", default_font)

        return custom_font_family
    else:
        raise ValueError("No font families found in the font file.")



#Startup


# Init startup logic
try:
    if not os.path.exists(DATA_FOLDER):
        print("Creating Data Folder")
        os.mkdir(DATA_FOLDER)
    if not os.path.exists(BACKUP_FOLDER):
        print("Creating TEMP_FOLDER_LOCATION")
        os.mkdir(BACKUP_FOLDER)
    custom_font_family = register_custom_font(window, "EUROCAPS.TTF")
    print("Directories created successfully")
except Exception as e:
    print("Error on startup:", e)


#Backup/Restore


def Backup():
    try:
        date = datetime.datetime.now().date()
        time = datetime.datetime.now().time()
        folder_name = f"{date}_{time.hour}_{time.minute}"
        shutil.copytree(
            KEYBIND_FOLDER, os.path.join(BACKUP_FOLDER, "Bindings", folder_name)
        )
        messagebox.showinfo(
            "KeepMyKeybinds", f"Backup saved to folder under '{folder_name}'"
        )
    except Exception as e:
        print("Error copying folders:", e)
        messagebox.showinfo("KeepMyKeybinds", e)


def Restore():
    print("Restoring")
    listdir = os.listdir(os.path.join(BACKUP_FOLDER, "Bindings"))
    listdir.sort()
    latest_backup = listdir[len(listdir) - 1]
    choice = messagebox.askokcancel(
        "KeepMyKeybinds!", f"Restore backup from {latest_backup}?"
    )
    if choice:
        shutil.rmtree(KEYBIND_FOLDER)
        shutil.copytree(
            os.path.join(BACKUP_FOLDER, "Bindings", latest_backup), KEYBIND_FOLDER
        )
        messagebox.showinfo(
            "KeepMyKeybinds!",
            "Sucessfully restored keybinds. Original backup has been kept",
        )
    else:
        return


def OpenBackupLocation():
    print(f"Opening backup location: " + DATA_FOLDER)
    subprocess.Popen(rf'explorer /select,"{BACKUP_FOLDER}"')

def OpenHelpPage():
    webbrowser.open_new_tab("https://niceygy.net/keepmykeybinds")


#GUI Conf



title = tk.Label(
    text="Keep My Keybinds!",
    anchor="center",
    fg="#f07b05",
    bg="black",
    font=("Euro Caps", 20),
).pack(fill="x")

tk.Label(
    text="A simple utility for managing keybinds \nfor elite. With 🩷 & 💥, by niceygy.",
    fg="#f07b05",
    bg="black",
    font=("Euro Caps", 13),
).pack(fill="x")

# BACKUP! & RESTORE! Button
BackupBtn = tk.Button(
    text="Manual Backup",
    fg="#f07b05",
    bg="black",
    command=Backup,
    font=("Euro Caps", 13),
).pack(fill="x")

RestoreBtn = tk.Button(
    text="Manual Restore",
    fg="#f07b05",
    bg="black",
    command=Restore,
    font=("Euro Caps", 13),
).pack(fill="x")

# # Tray Buttons

# ToggleTrayBtn = tk.Button(
#     text=f"{"Disable" if TRAY_ENABLED else "Enable"} backup checher",
#     fg="#f07b05",
#     bg="black",
#     font=("Euro Caps", 13),
#     command=toggle_tray
# ).pack(fill="x")
# tk.Label(
#     text="This will check for any changes when \nyour PC starts. May require admin \npermissions to enable.",
#     fg="#f07b05",
#     bg="black",
#     anchor="center",
#     font=("Euro Caps", 13),
# ).pack(fill="x")

# Open Backup Folder
OpenBackupBtn = tk.Button(
    text="Open backup Location",
    fg="#f07b05",
    bg="black",
    command=OpenBackupLocation,
    font=("Euro Caps", 13),
).pack(fill="x")
tk.Label(
    text="Opens the backup folder \nin file explorer",
    fg="#f07b05",
    bg="black",
    anchor="center",
    font=("Euro Caps", 13),
).pack(fill="x")

OpenHelpBtn = tk.Button(
    text="Help Me!",
    fg="#f07b05",
    bg="black",
    command=OpenHelpPage,
    font=("Euro Caps", 13),
).pack(fill="x")
tk.Label(
    text="Opens the help page \nin a browser",
    fg="#f07b05",
    bg="black",
    anchor="center",
    font=("Euro Caps", 13),
).pack(fill="x")



#Go!


window.mainloop()
