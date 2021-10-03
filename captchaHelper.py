from lib.AutoHotPy import AutoHotPy
from lib.InterceptionWrapper import InterceptionMouseState, InterceptionMouseStroke
import utils
import pytesseract
import cv2
import mss
import re
from PIL import Image

__captchaInputTemplate = cv2.imread("assets/captchaInput.png", cv2.IMREAD_GRAYSCALE)
__captchaCheckTemplate = cv2.imread("assets/captchaCheck.png", cv2.IMREAD_GRAYSCALE)

def __getCaptchaImageAndPoint(img):
    global __captchaInputTemplate
    captchaPoint = utils.detectTemplate(img, __captchaInputTemplate, 0.8, False)
    if not captchaPoint:
        return None

    templateHeight = __captchaInputTemplate.shape[0]
    templateWidth = __captchaInputTemplate.shape[1]
    captchaPointGlobal = utils.getGlobalPoint(captchaPoint[0], captchaPoint[1])
    captchaPointCenter = (int(captchaPointGlobal[0] + templateWidth / 2), int(captchaPointGlobal[1] + templateHeight / 2))
    
    y1 = captchaPoint[1] - 30
    y2 = captchaPoint[1] - 5
    x2 = captchaPoint[0] + 200

    captcha = img[y1:y2, captchaPoint[0]:x2]
    return (captcha, captchaPointCenter)

def __getCaptchaResult(text):
    text = text.replace('g', '8')
    text = text.replace('s', '8')
    text = text.replace('?', '7')

    findResult = re.findall(r'\d+', text)

    if len(findResult) > 2:
        findResult[0] += findResult[1]
        findResult.pop(1)

    sum = 0
    print(findResult)
    for digitStr in findResult:
        sum += int(digitStr)
    return sum

def __enterCaptcha(img, autohotpy, inputCenter, captcha):
    global __captchaCheckTemplate
    autohotpy.moveMouseToPosition(inputCenter[0], inputCenter[1])
    utils.minSleep()
    utils.leftClick(autohotpy)
    utils.minSleep()

    digits = utils.getNumberDigits(captcha);
    for digit in digits:
        utils.pressDigit(autohotpy, digit)

    checkPoint = utils.detectTemplatePivot(img, __captchaCheckTemplate, 0.8, (0.5, 0.5))
    if not checkPoint:
        return False
    autohotpy.moveMouseToPosition(checkPoint[0], checkPoint[1])
    utils.minSleep()
    utils.leftClick(autohotpy)
    return True

def __processImage(img):
    ret, threshold = cv2.threshold(img, 90, 255, cv2.THRESH_BINARY)

    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 3))
    dilation = cv2.dilate(threshold, rect_kernel, iterations = 1)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            threshold[0:threshold.shape[0], x:x + 78] = 0
            threshold[0:threshold.shape[0], x + w - 12:x + w] = 0

    contours, hierarchy = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contoursList = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        contoursList.append((x, cnt))
    contoursList.sort(key=lambda tup: tup[0], reverse=True)
    currX = contoursList[0][0]
    for i, tupl in enumerate(contoursList):
        delta = currX - tupl[0]
        if delta > 9:
            x, y, w, h = cv2.boundingRect(tupl[1])
            threshold[0:threshold.shape[0], x:x + w] = 0
            break
        currX = tupl[0]

    return threshold

def proceedCaptcha(autohotpy):
    screenImg = utils.grabImage()
    imageAndPoint = __getCaptchaImageAndPoint(screenImg)
    if not imageAndPoint:
        return False

    finalImage = __processImage(imageAndPoint[0])
    text = pytesseract.image_to_string(finalImage, config='--psm 11')

    result = __getCaptchaResult(text)
    success = __enterCaptcha(screenImg, autohotpy, imageAndPoint[1], result)
    return success

if __name__ == '__main__':
    captchaTest = cv2.imread('images/captchaImage6.png', cv2.IMREAD_GRAYSCALE)
    finalImage = __processImage(captchaTest)

    text = pytesseract.image_to_string(finalImage, config='--psm 11') # 4 6 7 10
    print(text)
    result = __getCaptchaResult(text)
    print(result)