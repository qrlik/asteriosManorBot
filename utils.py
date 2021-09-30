import cv2  # openCV
import numpy  # поддержка многомерных массивов | поддержка высокоуровневых математических функций
import json

__monitor = {"top": 0, "left": 0, "width": 0, "height": 0}

def init(config):
    global __monitor
    __monitor['top'] = int(config['resolutionHeight'] / 5)
    __monitor['height'] = int(config['resolutionHeight'] / 5 * 3)
    __monitor['left'] = 0
    __monitor['width'] = int(config['resolutionWidth'] / 4 * 3)

def getGlobalPoint(x, y):
    global __monitor
    return (x + __monitor['left'], y + __monitor['top'])

def grabImage():
    global __monitor
    with mss.mss() as screenshotManager:
        img = numpy.array(screenshotManager.grab(__monitor))
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def loadJsonFile(filename):
    try:
        with open(filename + '.json') as infile:
            return json.load(infile)
    except Exception as e:
        print('utils: loadJsonFile: ' + str(e))
        return None
