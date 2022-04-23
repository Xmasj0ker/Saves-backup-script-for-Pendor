import datetime
import msvcrt
import os
import os.path as op
import re
import shutil
import sys
import threading
from asyncio.windows_events import NULL
from time import sleep

import win32con
import win32gui

str0 = '/*如果你不清楚你在做什么，请不要修改此文件的任何内容并立刻关闭此文件*/'
hwnd = NULL


def main():
    setWindowTop()
    if not op.isfile('bak.ini'):
        initConfig()
    list = []
    with open('bak.ini', 'r', encoding='utf-8') as f:
        list = f.readlines()
    maxSaves = list[0][9:-1]
    sleepTime = list[1][10:-1]
    gameFile = list[2][9:-1]
    savePath = list[3][9:-1]
    saveFile = savePath + r'\last_savegame_backup.sav'
    if not op.exists(saveFile):
        error('未发现last_savegame_backup.sav文件，请检查bak.ini中路径是否正确')
    backPath = savePath + r'\bak'
    if not op.exists(backPath):
        os.makedirs(backPath)
    t1 = threading.Thread(target=thread, args=(maxSaves, sleepTime, saveFile, backPath))
    t1.start()
    os.popen(f'"{gameFile}"')
    setWindowMin()


def initConfig():
    maxSaves = 100
    sleepTime = 300
    gameFile = input('请拖入你常用的骑砍启动器文件并回车(一般是"mb_warband.exe"或者"WSELoader.exe"):\n').replace('"', '')
    savePath = input('请拖入你的存档文件夹并回车\n' + r'例如:C:\Users\Xmas\Documents\Mount&Blade Warband Savegames\Prophesy of Pendor V3.9.5' + '\n').replace('"', '')
    str = f'maxSaves:{maxSaves}\nsleepTime:{sleepTime}\ngamePath:{gameFile}\nsavePath:{savePath}\n{str0}'
    with open('bak.ini', 'w', encoding='utf-8') as f:
        f.write(str)


def thread(maxSaves, sleepTime, saveFile, backPath):
    modifyTime = ''
    while True:
        if modifyTime != os.stat(saveFile).st_mtime:
            bakList = os.listdir(backPath)
            bakList.sort()
            if len(bakList) > int(maxSaves):
                os.remove(f'{backPath}\\{bakList[0]}')
            bakFile = f'{backPath}\\{getBakName()}'
            shutil.copy(saveFile, bakFile)
            print(f'备份存档{op.basename(bakFile)}')
            modifyTime = os.stat(saveFile).st_mtime
        sleep(int(sleepTime))
    

def getBakName():
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d-%H-%M-%S') + '.sav'
    

def setWindowTop():
    global hwnd
    hwnd = win32gui.GetForegroundWindow()
    if hwnd != NULL:
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 960, 540, win32con.SWP_NOSIZE and win32con.SWP_NOMOVE)
    else:
        print('hwnd is null')


def setWindowMin():
    if hwnd != NULL:
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0, 960, 540, win32con.SWP_NOSIZE and win32con.SWP_NOMOVE)
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWMINIMIZED)
    else:
        print('hwnd is null')


def error(str):
    print(f'{str},按任意键关闭程序')
    msvcrt.getch()
    sys.exit()


main()
