from lib.AutoHotPy import AutoHotPy
from lib.InterceptionWrapper import InterceptionMouseState, InterceptionMouseStroke
import cv2  # openCV
import numpy  # поддержка многомерных массивов | поддержка высокоуровневых математических функций
import mss  # создания скриншотов
import json
import time

__monitor = {"top": 0, "left": 0, "width": 0, "height": 0}
__minDelay = 0.1

def minSleep():
    global __minDelay
    time.sleep(__minDelay)

def init(config):
    global __monitor
    __monitor['top'] = int(config['resolutionHeight'] / 5)
    __monitor['height'] = int(config['resolutionHeight'] / 5 * 3)
    __monitor['left'] = 0
    __monitor['width'] = int(config['resolutionWidth'] / 4 * 3)

def getGlobalPoint(x, y):
    global __monitor
    return (x + __monitor['left'], y + __monitor['top'])

def searchTemplate(source, template, factor):
    res = cv2.matchTemplate(source, template, cv2.TM_CCOEFF_NORMED)
    return numpy.where(res >= factor)

def grabImage():
    global __monitor
    with mss.mss() as screenshotManager:
        img = numpy.array(screenshotManager.grab(__monitor))
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def detectTemplate(source, template, factor, globalPos=True):
    loc = searchTemplate(source, template, factor)
    for point in zip(*loc[::-1]):
        #templateHeight = template.shape[0]
        #templateWidth = template.shape[1]
        #cv2.rectangle(img, point, (point[0] + templateWidth, point[1] + templateHeight), (0, 255, 0), 3)
        if globalPos:
            return getGlobalPoint(point[0], point[1])
        return point
    #cv2.imshow("test", img)
    #key = cv2.waitKey(1)
    return None

def detectTemplatePivot(source, template, factor, pivot, globalPos=True):
    point = detectTemplate(source, template, factor, globalPos)
    if not point:
        return None
    templateHeight = template.shape[0]
    templateWidth = template.shape[1]
    pointPivot = (int(point[0] + templateWidth * pivot[0]), int(point[1] + templateHeight * pivot[1]))
    return pointPivot

def leftClick(autohotpy):
    stroke = InterceptionMouseStroke()
    stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN
    autohotpy.sendToDefaultMouse(stroke)
    stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_UP
    autohotpy.sendToDefaultMouse(stroke)

def pressDigit(autohotpy, digit):
    if digit == 0:
        autohotpy.N0.press()
    elif digit == 1:
        autohotpy.N1.press()
    elif digit == 2:
        autohotpy.N2.press()
    elif digit == 3:
        autohotpy.N3.press()
    elif digit == 4:
        autohotpy.N4.press()
    elif digit == 5:
        autohotpy.N5.press()
    elif digit == 6:
        autohotpy.N6.press()
    elif digit == 7:
        autohotpy.N7.press()
    elif digit == 8:
        autohotpy.N8.press()
    elif digit == 9:
        autohotpy.N9.press()
    minSleep()

def getNumberDigits(number):
    digits = []
    numberStr = str(number)
    for digit in numberStr:
        digits.append(int(digit))
    return digits

def loadJsonFile(filename):
    try:
        with open(filename + '.json') as infile:
            return json.load(infile)
    except Exception as e:
        print('utils: loadJsonFile: ' + str(e))
        return None
