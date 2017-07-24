import win32api, win32gui, win32ui, win32con
from PIL import Image
from ctypes import *
import numpy as np
import pickle
import time
import cv2
import os

def windowHandle(newName, defaultName='iframe - Mozilla Firefox'):
    while True:
        try:
            h0 = win32gui.FindWindow(None, defaultName)
            win32gui.SetWindowPos(h0, None, 0, 0, 1012, 791, win32con.SWP_NOMOVE|win32con.SWP_NOZORDER|win32con.SWP_NOACTIVATE)
            print('Handle: ', h0)
            break
        except:
            print('ERROR: could not find handle.')
            time.sleep(5)
    h1 = 0
    while(h1 == 0):
        h1 = win32gui.FindWindowEx( h0, None, 'MozillaWindowClass', None)
        h2 = win32gui.FindWindowEx( h1, None, 'GeckoPluginWindow', None)
        h3 = win32gui.FindWindowEx( h2, None, 'GeckoFPSandboxChildWindow', None)
        time.sleep(1)
    time.sleep(2)
    win32gui.SetWindowText(h0, newName)
    return [h1, h3, h0]        
        
def leftClick(handle, coord, name, pause=1):
    x, y = [pos for pos in coord]
    lParam = (y << 16 | x)
    win32gui.SendMessage(handle, win32con.WM_LBUTTONDOWN, None, lParam)
    win32gui.SendMessage(handle, win32con.WM_LBUTTONUP, None, lParam)
    print('Clicked: ', name)
    time.sleep(pause)

def imageCap(handle):
    left, top, right, bot = win32gui.GetWindowRect(handle)
    w = right - left
    h = bot - top
    hwndDC = win32gui.GetWindowDC(handle)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)
    PW_RENDERFULLCONTENT = 2
    result = windll.user32.PrintWindow(handle, saveDC.GetSafeHdc(), PW_RENDERFULLCONTENT)
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    image = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(handle, hwndDC)
    if result == 1:
        return image

def imageSearch(obj, handle, method='cv2.TM_CCOEFF_NORMED'):
    method = eval(method)
    img = np.array(imageCap(handle))
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    path = 'Gray/' + obj + '.png'
    template = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(grayImg, template, method)
    threshold = .8
    loc = np.where( res >= threshold)
    if(len(loc[0]) == 0):
        print('Image not found')
        return False
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    coord = [int(round(top_left[0] + (w/2))), int(round(top_left[1] + (h/2)))]
    return coord

def imageClick(button, handle, pause=1):
    for tries in range(2):
        coord = imageSearch(button, handle[0])
        if(coord != False):
            leftClick(handle[1], coord, button, pause)
            return True
        else:
            time.sleep(2)
    return False

def load_obj(name):
    try:
        with open('statistics/' + name + '.pkl', 'rb') as f:
            return pickle.load(f)
    except:
        return False
    
def save_obj(stats, name):
    with open('statistics/' + name + '.pkl', 'wb') as f:
        pickle.dump(stats, f, pickle.HIGHEST_PROTOCOL)

def core(handle, newName, runs):
    fleetList1 = ('one', 'two', 'three', 'four', 'five',
              'six', 'seven', 'eight', 'nine')
    fleetList2 = ('ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifthteen')
    
    imageClick('cancel', handle, 3)
    imageClick('spaceBase', handle)
    if imageSearch('mail', handle[0]):
        imageClick('mail', handle)
        while imageSearch('pirate', handle[0]):
            imageClick('pirate', handle)
            imageClick('allCharge', handle)
            imageClick('deleteMail', handle)
        while imageSearch('reward', handle[0]):
            imageClick('reward', handle)
            imageClick('allCharge', handle)
            imageClick('deleteMail', handle)
        imageClick('exitMail', handle)
    for i in range(runs):
        imageClick('tutorial', handle)
        imageClick('restricted', handle)
        imageClick('enterR', handle)
        imageClick('normal', handle)
        imageClick('I27', handle)
        if not imageClick('Increase', handle):
            imageClick('IncreaseFleet', handle)
        imageClick('He3', handle)
        imageClick('SupplyAll', handle)
        imageClick('allConfirm', handle)
        if not imageClick('Increase', handle):
            imageClick('IncreaseFleet', handle)
        for fleet in fleetList1:
            imageClick(fleet, handle, .1)
        imageClick('fleetNext', handle)
        for fleet in fleetList2:
            imageClick(fleet, handle, .1)
        imageClick('OK', handle)
        if not imageClick('Goo', handle):
            imageClick('Go', handle)
        imageClick('spaceBase', handle)
        imageClick('MyTools', handle)
        imageClick('bag', handle)
        imageClick('items', handle)
        while(imageSearch('I27box', handle[0])):
            imageClick('I27box', handle)
            imageClick('use', handle)
            imageClick('collect', handle)
        imageClick('exitBag', handle)
        if not imageSearch('truced', handle[0]):
            imageClick('MyTools', handle)
            imageClick('bag', handle)
            imageClick('items', handle)
            if imageSearch('avdTruce', handle[0]):
                imageClick('avdTruce', handle)
                imageClick('use', handle)
            elif imageSearch('regularTruce', handle[0]):
                imageClick('regularTruce', handle)
                imageClick('use', handle)
            else:
                print('No truce found!')
            imageClick('exitBag', handle)
        while not imageSearch('mail', handle[0]):
            time.sleep(10)
        imageClick('mail', handle)
        if not imageSearch('reward', handle[0]):
            time.sleep(120)
        while imageSearch('pirate', handle[0]):
            imageClick('pirate', handle)
            imageClick('allCharge', handle)
            imageClick('deleteMail', handle)
        while imageSearch('reward', handle[0]):
            imageClick('reward', handle)
            imageClick('allCharge', handle)
            imageClick('deleteMail', handle)

        imageClick('exitMail', handle)
            
            
def main():
    loginInfo = open('config/iframe.txt', 'r')
    newName = loginInfo.readline()
    newName = newName.rstrip()
    url = loginInfo.readline()
    print('windowName: ', newName, ' ', 'url: ', url)
    command = 'start firefox.exe \"' + url + '\"'
    os.popen(command)
    time.sleep(5)
    handle = windowHandle(newName)
    print(handle)
    runs = int(input('runs for refresh: '))
    while True:
        core(handle, newName, runs)
        temp = (handle[2], handle[2])
        imageClick('playGame', temp)
        time.sleep(20)
        handle = windowHandle(newName, newName)
        
main()
    
