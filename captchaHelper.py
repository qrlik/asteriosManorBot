import utils
import pytesseract
import cv2
import mss
import re
from PIL import Image

__captchaInputTemplate = cv2.imread("assets/captchaInput.png", cv2.IMREAD_GRAYSCALE)

def __getCaptchaImage():
    global __captchaInputTemplate
    img = utils.grabImage()
    cv2.imwrite('images/grabForCaptcha.png', img)
    captchaPoint = utils.detectTemplate(img, __captchaInputTemplate, 0.8, False)
    if not captchaPoint:
        return None
    y1 = captchaPoint[1] - 30
    y2 = captchaPoint[1] - 5
    x2 = captchaPoint[0] + 200
    return img[y1:y2, captchaPoint[0]:x2]

def __getCaptchaResult(text):
    findResult = re.findall(r'\d+', text)
    sum = 0
    for digitStr in findResult:
        sum += int(digitStr)
    return sum

def proceedCaptcha():
    img = __getCaptchaImage()
    if type(img) == None:
        return False
    cv2.imwrite('images/captchaImage.png', img)
    ret, threshold = cv2.threshold(img, 140, 255, cv2.THRESH_BINARY)
    cv2.imwrite('images/captchaImageThreshold.png', threshold)
    text = pytesseract.image_to_string(threshold, lang='eng', config='--psm 7')
    result = __getCaptchaResult(text)
    return True