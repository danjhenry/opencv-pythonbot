import win32api, win32gui, win32ui, win32con
from PIL import Image
from ctypes import *
import numpy as np
import cv2
import os
import time

#Physical Locations
wepCenterLoc = [606, 133]
tradeCenterLoc = [80, 400]
comCenterLoc = [262, 153]
techCenterLoc = [420, 70]
sellBox = [735, 295]

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
    return [h1, h3]        
        
def leftClick(handle, coord, name, pause=1):
    x, y = [pos for pos in coord]
    lParam = (y << 16 | x)
    win32gui.SendMessage(handle, win32con.WM_LBUTTONDOWN, None, lParam)
    win32gui.SendMessage(handle, win32con.WM_LBUTTONUP, None, lParam)
    print('Clicked: ', name)
    time.sleep(pause)
    
def sellItem(handle, string):
    leftClick(handle, sellBox, 'sellBox', 0)
    for char in string:
        win32api.SendMessage(handle, win32con.WM_CHAR, ord(char), None)

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

def construct(loc, handle, building, tab):
    imageClick('build', handle)
    imageClick('constructBuilding', handle)
    imageClick(tab, handle)
    if(imageClick(building, handle) == False):
        imageClick('comExit', handle)
        return False
    leftClick(handle[1], loc, building)
    if(building != 'weaponCenterB'):
        imageClick('upgradeArrow', handle)
        imageClick('voucherOk', handle)

def wheelSpin(handle):
    spins = 0
    while True:
        spins += 1
        if(imageSearch('exitFriend', handle[0])):
            imageClick('exitFriend', handle)
        imageClick('buyAndSpin', handle)
        time.sleep(10)
        if(imageClick('wheelOk', handle) == False):
            break
        imageClick('spinNow', handle)
    return spins 

def core(handle, newName):
    openables = ('skillBoat', 'superCase', 'superBoat')
    cardTypes = ('skill', 'Super', 'legendary', 'Superstar')
    total = 0
    while True:
        imageClick('beginOk', handle, 5)
        imageClick('cancel', handle, 3)
        imageClick('mail', handle)
        if(imageClick('welcome', handle) == False):
            imageClick('selectAll', handle)  
        imageClick('deleteMail', handle)
        imageClick('deleteMailOk', handle)
        imageClick('exitMail', handle)
        imageClick('warehouse', handle)
        imageClick('harvest', handle)
        imageClick('MyTools', handle)
        imageClick('Quest', handle)
        imageClick('getQuest', handle)
        imageClick('exitQuest', handle)
        construct(comCenterLoc, handle, 'commandCenterB', 'military')
        imageClick('commandCenter', handle)
        imageClick('commandCenterEnter', handle)
        imageClick('drawCom', handle)
        imageClick('comExit', handle)
        imageClick('spaceBase', handle)
        imageClick('tutorial', handle)
        imageClick('luckyWheel', handle)
        imageClick('spinNow', handle, 11)
        imageClick('wheelOk', handle, 1)
        imageClick('spinNow', handle, 1)
        imageClick('voucherCheck', handle)
        total += wheelSpin(handle)
        imageClick('spinEnd', handle)
        imageClick('MyTools', handle)
        imageClick('bag', handle)
        for item in (openables + cardTypes):
            if(imageSearch(item, handle[0])):
                error = False
                for case in openables:
                    if(imageSearch(case, handle[0])):
                        imageClick(case, handle)
                        if(imageClick('use', handle) == False):
                            imageClick('spinEnd', handle)
                            error = True
                            break
                        else:
                            imageClick('collect', handle)  
                if(error):
                    break
                imageClick('exitBag', handle)
                imageClick('groundBase', handle)
                imageClick('civicCenter', handle)
                imageClick('upgrade', handle)
                imageClick('upgradeArrow', handle)
                imageClick('voucherOk', handle)
                construct(wepCenterLoc, handle, 'weaponCenterB', 'military')
                time.sleep(41)
                construct(techCenterLoc, handle, 'techCenterB', 'cityServices')
                construct(tradeCenterLoc, handle, 'tradeCenterB', 'cityServices')
                imageClick('social', handle)
                imageClick('AH', handle)
                imageClick('Sell', handle)
                imageClick('card', handle)
                imageClick('sellPrice', handle)
                for card in cardTypes:
                    while(imageSearch(card, handle[0])):
                        imageClick(card, handle)
                        imageClick('sellBox', handle)
                        sellItem(handle[1], '1')
                        imageClick('finalSell', handle)
                imageClick('comExit', handle, 10)
                while True:
                    if(imageSearch('mail', handle[0])):
                        time.sleep(20)
                        imageClick('mail', handle)
                        while(imageSearch('sale', handle[0])):
                            imageClick('sale', handle) 
                            imageClick('deleteMail', handle)
                            imageClick('deleteMailOk', handle)
                        imageClick('exitMail', handle)
                        imageClick('spaceBase', handle)
                        break
                    time.sleep(10)
                if(error == False):
                    break
        print('No commanders in bag.')
        imageClick('exitBag', handle)
        if(imageClick('galaxy', handle) == False):
            imageClick('galaxy2', handle)
        imageClick('ursa', handle)
        imageClick('abandonPlanet', handle, 1)
        imageClick('abandonOk', handle)
        imageClick('abandonOk2', handle, 5)
        handle = windowHandle(newName, newName)
        if(imageSearch('failed', handle[0])):
            imageClick('mailLeft', handle)
            imageClick('Return', handle)
            imageClick('MyTools', handle)
            imageClick('toolMail', handle)
            if(imageClick('selectAll', handle) == False):
                while(imageClick('welcome', handle) or imageClick('sale', handle)):
                    imageClick('deleteMail', handle)
                    imageClick('deleteMailOk', handle)
            imageClick('deleteMail', handle)
            imageClick('deleteMailOk', handle)
            imageClick('exitMail', handle)
            imageClick('galaxy', handle)
            imageClick('ursa', handle)
            imageClick('abandonPlanet', handle)
            imageClick('abandonOk', handle)
            imageClick('abandonOk2', handle, 5)
            handle = windowHandle(newName, newName)
        print('Total number of vouchers used ', total*5) 
        time.sleep(15)

def main():
    loginInfo = open('config/iframe.txt', 'r')
    newName = loginInfo.readline()
    url = loginInfo.readline()
    print('windowName: ', newName, ' ', 'url: ', url)
    command = 'start firefox.exe \"' + url + '\"'
    os.popen(command)
    time.sleep(5)
    handle = windowHandle(newName)
    print(handle)
    core(handle, newName)
main()
    
