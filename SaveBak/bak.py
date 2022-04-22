from asyncio.windows_events import NULL
import os
import win32gui, win32con
import msvcrt

def main():
    os.system('where python')
    print('hello')
    setWindowTop()
    msvcrt.getch()


def setWindowTop():
    hwnd = win32gui.FindWindow(None, "C:\Windows\py.exe")
    if(hwnd != NULL):
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 960, 540, win32con.SWP_NOSIZE and win32con.SWP_NOMOVE)


main()