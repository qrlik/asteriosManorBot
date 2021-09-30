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

def searchTemplate(template, factor):
    img = grabImage()
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    return numpy.where(res >= factor)

def detectTemplate(template, factor):
    loc = searchTemplate(template, factor)
    for point in zip(*loc[::-1]):
        #templateHeight = template.shape[0]
        #templateWidth = template.shape[1]
        #cv2.rectangle(img, point, (point[0] + templateWidth, point[1] + templateHeight), (0, 255, 0), 3)
        return getGlobalPoint(point[0], point[1])
    #cv2.imshow("test", img)
    #key = cv2.waitKey(1)
    return None

def detectTemplatePivot(template, factor, pivot):
    point = detectTemplate(template, factor)
    if not point:
        return None
    templateHeight = template.shape[0]
    templateWidth = template.shape[1]
    pointPivot = (int(point[0] + templateWidth * pivot[0]), int(point[1] + templateHeight * pivot[1]))
    return pointPivot

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
