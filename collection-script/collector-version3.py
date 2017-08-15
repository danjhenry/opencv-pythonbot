import win32api, win32gui, win32ui, win32con
from PIL import Image
from ctypes import *
import numpy as np
import cv2
import os
import time

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
    while h1 == 0:
        h1 = win32gui.FindWindowEx( h0, None, 'MozillaWindowClass', None)
        h2 = win32gui.FindWindowEx( h1, None, 'GeckoPluginWindow', None)
        h3 = win32gui.FindWindowEx( h2, None, 'GeckoFPSandboxChildWindow', None)
        time.sleep(1)
    time.sleep(2)
    win32gui.SetWindowText(h0, newName)
    return [h1, h3]        
        
def leftClick(handle, coord, name, pause=.5):
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
    if len(loc[0]) == 0:
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
        if coord:
            leftClick(handle[1], coord, button, pause)
            return True
        else:
            time.sleep(2)
    return False

def core(handle, newName):
    imageClick('cancel', handle)
    imageClick('social', handle)
    imageClick('AH', handle)
    totalCollected = 0
    while True:
        if totalCollected >= 40:
            imageClick('exit', handle)
            imageClick('mail', handle)
            while imageSearch('purchaseSuccessful', handle[0]):
                imageClick('purchaseSuccessful', handle)
                imageClick('allCharge', handle)
                imageClick('deleteMail', handle)
            imageClick('exit', handle)
            imageClick('social', handle)
            imageClick('AH', handle)
            totalCollected = 0
            
        imageClick('card', handle)
        if imageSearch('endOfList', handle[0]):
            imageClick('endOfList', handle)
        for x in range(5):
            for x in range(5):
                if imageSearch('buy', handle[0]):
                    imageClick('buy', handle)
                    imageClick('purchase', handle)
                    if imageClick('buyOk', handle):
                        totalCollected += 1
                        break
                else:
                    break
            if imageSearch('MP', handle[0]):
                print('mp found')
                break
            if imageSearch('nextPage', handle[0]):
                imageClick('nextPage', handle)
       
def main():
    loginInfo = open('config/iframe.txt', 'r')
    newName = loginInfo.readline()
    url = loginInfo.readline()
    print('windowName: ', newName, ' ', 'url: ', url)
    command = 'start firefox.exe \"' + url + '\"'
    os.popen(command)
    time.sleep(15)
    handle = windowHandle(newName)
    print(handle)
    core(handle, newName)
main()
    
