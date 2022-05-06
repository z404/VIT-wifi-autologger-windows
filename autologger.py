# Creates a task-bar icon.  Run from Python.exe to see the
# messages printed.
import win32api, win32gui
import win32con, winerror
import sys, os
import subprocess
import requests
from requests.structures import CaseInsensitiveDict
from dotenv import dotenv_values

config = dotenv_values()


class MainWindow:
    def __init__(self):
        msg_TaskbarRestart = win32gui.RegisterWindowMessage("TaskbarCreated")
        message_map = {
            msg_TaskbarRestart: self.OnRestart,
            win32con.WM_DESTROY: self.OnDestroy,
            win32con.WM_COMMAND: self.OnCommand,
            win32con.WM_USER + 20: self.OnTaskbarNotify,
        }
        # Register the Window class.
        wc = win32gui.WNDCLASS()
        hinst = wc.hInstance = win32api.GetModuleHandle(None)
        wc.lpszClassName = "VITWifiAutologger"
        wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        wc.hCursor = win32api.LoadCursor(0, win32con.IDC_ARROW)
        wc.hbrBackground = win32con.COLOR_WINDOW
        wc.lpfnWndProc = message_map  # could also specify a wndproc.

        # Don't blow up if class already registered to make testing easier
        try:
            classAtom = win32gui.RegisterClass(wc)
        except win32gui.error as err_info:
            if err_info.winerror != winerror.ERROR_CLASS_ALREADY_EXISTS:
                raise

        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(
            wc.lpszClassName,
            "Options",
            style,
            0,
            0,
            win32con.CW_USEDEFAULT,
            win32con.CW_USEDEFAULT,
            0,
            0,
            hinst,
            None,
        )
        win32gui.UpdateWindow(self.hwnd)
        self._DoCreateIcons()

    def _DoCreateIcons(self):
        # Try and find a custom icon
        hinst = win32api.GetModuleHandle(None)
        try:
            iconPathName = os.path.abspath(os.path.join(os.path.join(os.getcwd(), "icon"), "logo.ico"))
        except:
            iconPathName = os.path.abspath(
                os.path.join(os.path.split(sys.executable)[0], "pyc.ico")
            )
        print(iconPathName)
        if not os.path.isfile(iconPathName):
            # Look in DLLs dir, a-la py 2.5
            iconPathName = os.path.abspath(
                os.path.join(os.path.split(sys.executable)[0], "DLLs", "pyc.ico")
            )
        if not os.path.isfile(iconPathName):
            # Look in the source tree.
            iconPathName = os.path.abspath(
                os.path.join(os.path.split(sys.executable)[0], "..\\PC\\pyc.ico")
            )
        if os.path.isfile(iconPathName):
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = win32gui.LoadImage(
                hinst, iconPathName, win32con.IMAGE_ICON, 0, 0, icon_flags
            )
            print(hicon)
        else:
            print("Can't find a Python icon file - using default")
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER + 20, hicon, "VIT Wifi Autologger")
        try:
            win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
        except win32gui.error:
            # This is common when windows is starting, and this code is hit
            # before the taskbar has been created.
            print("Failed to add the taskbar icon - is explorer running?")
            # but keep running anyway - when explorer starts, we get the
            # TaskbarCreated message.

    def OnRestart(self, hwnd, msg, wparam, lparam):
        self._DoCreateIcons()

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)  # Terminate the app.

    def OnTaskbarNotify(self, hwnd, msg, wparam, lparam):
        if lparam == win32con.WM_LBUTTONUP:
            # print("You clicked me.")
            wifi = subprocess.check_output(['netsh', 'WLAN', 'show', 'interfaces'])
            data = wifi.decode('utf-8')
            if "VIT2.4G" in data or "VIT5G" in data:
                print("Connected to VIT Wifi!")
                url = "http://phc.prontonetworks.com/cgi-bin/authlogin?URI=http://www.msftconnecttest.com/redirect"

                headers = CaseInsensitiveDict()
                headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9"
                headers["Accept-Language"] = "en-US,en;q=0.9"
                headers["Cache-Control"] = "max-age=0"
                headers["Connection"] = "keep-alive"
                headers["Content-Type"] = "application/x-www-form-urlencoded"
                headers["Origin"] = "http://phc.prontonetworks.com"
                headers["Referer"] = "http://phc.prontonetworks.com/cgi-bin/authlogin?URI=http://google.com/"
                headers["Sec-GPC"] = "1"
                headers["Upgrade-Insecure-Requests"] = "1"
                headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"

                data = "userId="+config["username"]+"&password="+config["password"]+"&serviceName=ProntoAuthentication&Submit22=Login"


                resp = requests.post(url, headers=headers, data=data)
                if resp.status_code == 200:
                    print("Logged in!")
                else:
                    print("Failed to login!")
            else:
                print("Not connected to VIT wifi")

        # elif lparam == win32con.WM_LBUTTONDBLCLK:
        #     # print("You double-clicked me - goodbye")
        #     # win32gui.DestroyWindow(self.hwnd)
        #     requests.get("http://phc.prontonetworks.com/cgi-bin/authlogout?blank=")
        #     print("Logged out!")
        elif lparam == win32con.WM_RBUTTONUP:
            print("You right clicked me.")
            menu = win32gui.CreatePopupMenu()
            win32gui.AppendMenu(menu, win32con.MF_STRING, 1023, "Login to Wifi")
            win32gui.AppendMenu(menu, win32con.MF_STRING, 1024, "Log Out of Wifi")
            win32gui.AppendMenu(menu, win32con.MF_STRING, 1025, "Exit program")
            pos = win32gui.GetCursorPos()
            # See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winui/menus_0hdi.asp
            win32gui.SetForegroundWindow(self.hwnd)
            win32gui.TrackPopupMenu(
                menu, win32con.TPM_LEFTALIGN, pos[0], pos[1], 0, self.hwnd, None
            )
            win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)
        return 1

    def OnCommand(self, hwnd, msg, wparam, lparam):
        id = win32api.LOWORD(wparam)
        if id == 1023:
            wifi = subprocess.check_output(['netsh', 'WLAN', 'show', 'interfaces'])
            data = wifi.decode('utf-8')
            if "VIT2.4G" in data or "VIT5G" in data:
                print("Connected to VIT Wifi!")
                url = "http://phc.prontonetworks.com/cgi-bin/authlogin?URI=http://www.msftconnecttest.com/redirect"

                headers = CaseInsensitiveDict()
                headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9"
                headers["Accept-Language"] = "en-US,en;q=0.9"
                headers["Cache-Control"] = "max-age=0"
                headers["Connection"] = "keep-alive"
                headers["Content-Type"] = "application/x-www-form-urlencoded"
                headers["Origin"] = "http://phc.prontonetworks.com"
                headers["Referer"] = "http://phc.prontonetworks.com/cgi-bin/authlogin?URI=http://google.com/"
                headers["Sec-GPC"] = "1"
                headers["Upgrade-Insecure-Requests"] = "1"
                headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"

                data = "userId="+config["username"]+"&password="+config["password"]+"&serviceName=ProntoAuthentication&Submit22=Login"


                resp = requests.post(url, headers=headers, data=data)
                if resp.status_code == 200:
                    print("Logged in!")
                else:
                    print("Failed to login!")
            else:
                print("Not connected to VIT wifi")
        elif id == 1024:
            requests.get("http://phc.prontonetworks.com/cgi-bin/authlogout?blank=")
            print("Logged out!")
        elif id == 1025:
            print("Goodbye")
            win32gui.DestroyWindow(self.hwnd)
        else:
            print("Unknown command -", id)


def main():
    w = MainWindow()
    win32gui.PumpMessages()


if __name__ == "__main__":
    main()