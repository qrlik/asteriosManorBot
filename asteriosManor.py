from lib.AutoHotPy import AutoHotPy
from lib.InterceptionWrapper import InterceptionMouseState, InterceptionMouseStroke
from pynput import keyboard  # слушатель ввода
import numpy  # поддержка многомерных массивов | поддержка высокоуровневых математических функций
import cv2  # openCV
import mss  # создания скриншотов
import utils
import time
import threading

__config = {}
__delay = 0.16
__monitor = {"top": 0, "left": 0, "width": 0, "height": 0}
__paused = True
__chatWindowTemplate = None
__autoPy = AutoHotPy()
    
def __init():
    __chatWindowTemplate = cv2.imread("assets/chatScroll.png", cv2.IMREAD_GRAYSCALE)
    __config = utils.loadJsonFile('config')

    __monitor['top'] = int(__config['resolutionHeight'] / 5)
    __monitor['height'] = int(__config['resolutionHeight'] / 5 * 3)
    __monitor['left'] = 0
    __monitor['width'] = int(__config['resolutionWidth'] / 4 * 3)

def __getGlobalPoint(x, y):
    return (x + __monitor['left'], y + __monitor['top'])

def __checkPause():
    while __paused:
        time.sleep(3)
    return

def __openChatWindow():
    __checkPause()
    __autoPy.F1.press()
    __autoPy.F1.press()
    time.sleep(__delay)

def __detectChatWindowScroll():
    with mss.mss() as screenshotManager:
        while True:
            __checkPause()
            img = numpy.array(screenshotManager.grab(__monitor))
            processedImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            res = cv2.matchTemplate(processedImage, __chatWindowTemplate, cv2.TM_CCOEFF_NORMED)
            loc = numpy.where(res >= 0.9)

            for point in zip(*loc[::-1]):
                templateHeight = __chatWindowTemplate.shape[0]
                templateWidth = __chatWindowTemplate.shape[1]

                #cv2.rectangle(img, point, (point[0] + templateWidth, point[1] + templateHeight), (0, 255, 0), 3)
                #cv2.imshow("test", img)
                #key = cv2.waitKey(1)
                    
                scrollPoint = __getGlobalPoint(point[0], point[1])
                scrollMiddlePoint = (int(scrollPoint[0] + templateWidth / 2), int(scrollPoint[1] + templateHeight / 2))
                return scrollMiddlePoint
            time.sleep(__delay)

def __scrollChatWindow(point):
    __checkPause()
    __autoPy.moveMouseToPosition(point[0], point[1])
    stroke = InterceptionMouseStroke()
    stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN
    autohot_py.sendToDefaultMouse(stroke)
    __autoPy.moveMouseToPosition(point[0], point[1] + 295)
    stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_RIGHT_BUTTON_UP
    autohot_py.sendToDefaultMouse(stroke)
    time.sleep(__delay)

def proceed(autohotpy, event):
    __checkPause()
    #with pyautogui.hold('shift'):

    __openChatWindow()
    scrollPoint = __detectChatWindowScroll()
    __scrollChatWindow(scrollPoint)

    autohotpy.run(proceed, event)

def run():
    __init()
    __autoPy.registerExit(__autoPy.END, __onExit)
    __autoPy.registerForKeyDown(__autoPy.F12, __switchPause)
    __autoPy.start()


def __onExit(autohotpy, event):
    autohotpy.stop()

def __switchPause(autohotpy, event):
    global __paused

    __paused = not __paused
    print('Paused' if __paused else 'Resumed')
    if not __paused:
        proceed(autohotpy, event)


def main():
    run()

if __name__ == '__main__':
    main()

