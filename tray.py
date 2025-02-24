import datetime
import os
import shutil
# import wx
import wx.adv


TASKTRAY_NAME = "KeepMyKeybinds!"
TASKTRAY_MESSAGE = "Backup in progress..."
TASKTRAY_ICON = 'icon.png'


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item


class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self):
        super(TaskBarIcon, self).__init__()
        self.set_icon(TASKTRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, TASKTRAY_MESSAGE, self.say_hello)
        create_menu_item(menu, "This will close once the backup is done", self.say_hello)
        create_menu_item(menu, "Open the main app to enable/disable this!", self.say_hello)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.Icon(path, wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon, TASKTRAY_NAME)

    def on_left_down(self, event):
        return

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)

    def say_hello(self, event):
        return


def main():
    app = wx.App()
    TaskBarIcon()
    app.MainLoop()
    CONFIG_LOCATION = "C:\\Users\\" + os.getlogin() + "\\AppData\\Local\\Frontier Developments\\Elite Dangerous\\Options\\"
    KEYBIND_FOLDER = CONFIG_LOCATION + "Bindings\\"
    DATA_FOLDER = "C:\\Users\\" + os.getlogin() + "\\.KeepMyKeybinds\\"
    BACKUP_FOLDER = DATA_FOLDER + "backups\\"

    try:
        date = datetime.datetime.now().date()
        time = datetime.datetime.now().time()
        folder_name = f"{date}_{time.hour}_{time.minute}"
        shutil.copytree(KEYBIND_FOLDER, os.path.join(BACKUP_FOLDER, "Bindings", folder_name))
    except Exception as e:
        print("Error in tray:", e)
    
    while True:
        time.sleep(100)

if __name__ == '__main__':
    main()