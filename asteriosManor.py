from lib.AutoHotPy import AutoHotPy
from lib.InterceptionWrapper import InterceptionMouseState, InterceptionMouseStroke
from pynput import keyboard  # слушатель ввода
import numpy  # поддержка многомерных массивов | поддержка высокоуровневых математических функций
import cv2  # openCV
import mss  # создания скриншотов
import utils
import time

__autoPy = AutoHotPy()
__chatScrollTemplate = cv2.imread("assets/chatScroll.png", cv2.IMREAD_GRAYSCALE)
__config = utils.loadJsonFile('config')
__delay = 0.0
__paused = True
    
def __init():
    global __config
    global __delay
    __delay = __config['delay']
    utils.init(__config)

def __openChatWindow():
    global __autoPy
    global __delay
    __autoPy.F1.press()
    __autoPy.F1.press()
    time.sleep(__delay)

def __detectChatWindowScroll():
    global __monitor
    global __chatScrollTemplate
    global __delay
    while True:
        img = utils.grabImage()
        loc = utils.searchTemplate(img, __chatScrollTemplate, 0.9)

        for point in zip(*loc[::-1]):
            templateHeight = __chatScrollTemplate.shape[0]
            templateWidth = __chatScrollTemplate.shape[1]
            #cv2.rectangle(img, point, (point[0] + templateWidth, point[1] + templateHeight), (0, 255, 0), 3) #debug
            scrollPoint = utils.getGlobalPoint(point[0], point[1])
            scrollMiddlePoint = (int(scrollPoint[0] + templateWidth / 2), int(scrollPoint[1] + templateHeight / 2))
            return scrollMiddlePoint
        #cv2.imshow("test", img) #debug
        #key = cv2.waitKey(1)
        time.sleep(__delay)

def __scrollChatWindow(point):
    global __autoPy
    global __delay
    __autoPy.moveMouseToPosition(point[0], point[1])
    stroke = InterceptionMouseStroke()
    stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN
    __autoPy.sendToDefaultMouse(stroke)
    time.sleep(__delay)
    __autoPy.moveMouseToPosition(point[0], point[1] + 295)
    stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_UP
    __autoPy.sendToDefaultMouse(stroke)
    time.sleep(__delay)

def __openCaptchaWindow(point):
    global __autoPy
    global __delay
    __autoPy.moveMouseToPosition(point[0] - 195, point[1] + 100)
    stroke = InterceptionMouseStroke()
    stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN
    autohotpy.sendToDefaultMouse(stroke)
    stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_UP
    autohotpy.sendToDefaultMouse(stroke)
    time.sleep(__delay)
       

def proceed(autohotpy, event):
    global __paused
    #with pyautogui.hold('shift'):
    __openChatWindow()
    scrollPoint = __detectChatWindowScroll()
    __scrollChatWindow(scrollPoint)
    __openCaptchaWindow(scrollPoint)
    if not __paused:
        autohotpy.run(proceed, event)

def __switchPause(autohotpy, event):
    global __paused
    __paused = not __paused
    print('Paused' if __paused else 'Resumed')
    if not __paused:
        proceed(autohotpy, event)

def __onExit(autohotpy, event):
    global __paused
    __paused = True
    autohotpy.stop()

def run():
    global __autoPy
    __init()
    __autoPy.registerForKeyDown(__autoPy.F11, __switchPause)
    __autoPy.registerExit(__autoPy.ESC, __onExit)
    __autoPy.start()

    

def main():
    run()

    #__init() # debug
    #proceed(None, None)

if __name__ == '__main__':
    main()

