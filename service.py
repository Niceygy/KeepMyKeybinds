import datetime
import os
import shutil
from windowsservice import BaseService
import servicemanager


class KeybindBackupService(BaseService):
    _svc_name_ = "KeepMyKeybinds"
    _svc_display_name_ = "KeepMyKeybinds!"
    _svc_description_ = "A service to automatically backup keybinds for Elite Dangerous."

    def __init__(self, args):
        super().__init__(args)
        self.is_running = True

    def stop(self):
        self.is_running = False

    def is_running(self):
        return self.is_running

    def main(self):
        CONFIG_LOCATION = "C:\\Users\\" + os.getlogin() + "\\AppData\\Local\\Frontier Developments\\Elite Dangerous\\Options\\"
        KEYBIND_FOLDER = CONFIG_LOCATION + "Bindings\\"
        DATA_FOLDER = "C:\\Users\\" + os.getlogin() + "\\.KeepMyKeybinds\\"
        BACKUP_FOLDER = DATA_FOLDER + "backups\\"

        while self.is_running:
            try:
                date = datetime.datetime.now().date()
                time = datetime.datetime.now().time()
                folder_name = f"{date}_{time.hour}_{time.minute}"
                shutil.copytree(KEYBIND_FOLDER, os.path.join(BACKUP_FOLDER, "Bindings", folder_name))
                time.sleep(60)  # Check for changes every minute
            except Exception as e:
                print("Error in service:", e)
                time.sleep(60)

if __name__ == '__main__':
    servicemanager.Initialize()
    servicemanager.PrepareToHostSingle(KeybindBackupService)
    servicemanager.StartServiceCtrlDispatcher()