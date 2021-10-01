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
    cv2.imwrite('images/grabForCaptcha.png', img)
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
    return (img[y1:y2, captchaPoint[0]:x2], captchaPointCenter)

def __getCaptchaResult(text):
    findResult = re.findall(r'\d+', text)
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
    
    print(captcha)
    print(digits)

    for digit in digits:
        utils.pressDigit(autohotpy, digit)

    checkPoint = utils.detectTemplatePivot(img, __captchaCheckTemplate, 0.8, (0.5, 0.5))
    if not checkPoint:
        return False
    autohotpy.moveMouseToPosition(checkPoint[0], checkPoint[1])
    utils.minSleep()
    utils.leftClick(autohotpy)
    return True

def proceedCaptcha(autohotpy):
    screenImg = utils.grabImage()
    imageAndPoint = __getCaptchaImageAndPoint(screenImg)
    if not imageAndPoint:
        return False
    
    cv2.imwrite('images/captchaImage.png', imageAndPoint[0])
    ret, threshold = cv2.threshold(imageAndPoint[0], 140, 255, cv2.THRESH_BINARY)
    cv2.imwrite('images/captchaImageThreshold.png', threshold)
    text = pytesseract.image_to_string(threshold)

    result = __getCaptchaResult(text)
    success = __enterCaptcha(screenImg, autohotpy, imageAndPoint[1], result)
    return success