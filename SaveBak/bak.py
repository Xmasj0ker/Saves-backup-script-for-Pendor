from asyncio.windows_events import NULL
import os.path as op
from time import sleep
import win32gui, win32con
import msvcrt
import threading
import sys

str0 = '/*如果你不清楚你在做什么，请不要修改此文件的任何内容并立刻关闭此文件*/'
maxSaves = 0
gamePath = ''
savePath = ''


def main():
    t1 = threading.Thread(target=thread)
    t1.start()
    print('hello')
    setWindowTop()
    msvcrt.getch()


def thread():
    print('i sleep')
    sleep(2)
    print('i wake up')


def readConfig():
    if(not op.isfile('bak.ini')):
        initConfig()
    global maxSaves
    global gamePath
    global savePath
    list = []
    with open('bak.ini', 'r', encoding='utf-8') as f:
        list = f.readlines()
    maxSaves = list[0][9:-1]
    gamePath = list[1][9:-1]
    savePath = list[2][9:-1] + r'\last_savegame_backup.sav'


def initConfig():
    global maxSaves
    global gamePath
    global savePath
    maxSaves = 100
    gamePath = input('请拖入你常用的骑砍启动器文件并回车(一般是"mb_warband.exe"或者"WSELoader.exe"):\n')
    savePath = input('请拖入你的存档文件夹并回车\n' + r'例如:C:\Users\Xmas\Documents\Mount&Blade Warband Savegames\Prophesy of Pendor V3.9.5' + '\n')
    str = f'maxSaves:{maxSaves}\ngamePath:{gamePath}\nsavePath:{savePath}\n{str0}'
    with open('bak.ini', 'w', encoding='utf-8') as f:
        f.write(str)


def setWindowTop():
    hwnd = win32gui.FindWindow(None, "C:\Windows\py.exe")
    if(hwnd != NULL):
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 960, 540, win32con.SWP_NOSIZE and win32con.SWP_NOMOVE)


def error(str):
    print(f'{str},按任意键关闭程序')
    msvcrt.getch()
    sys.exit()


main()