from lib.AutoHotPy import AutoHotPy
from lib.InterceptionWrapper import InterceptionMouseState, InterceptionMouseStroke
import cv2  # openCV
import utils
import time
import captchaHelper
import manorHelper

__autoPy = AutoHotPy()
__chatScrollTemplate = cv2.imread("assets/chatScroll.png", cv2.IMREAD_GRAYSCALE)
__chatButtonTemplate = cv2.imread("assets/chatButton.png", cv2.IMREAD_GRAYSCALE)
__paused = True
    
def __openChatWindow():
    global __autoPy
    __autoPy.F1.press()
    utils.minSleep()
    __autoPy.F1.press()
    utils.sleep()

def __scrollChatWindow(point):
    global __autoPy
    __autoPy.moveMouseToPosition(point[0], point[1])
    stroke = InterceptionMouseStroke()
    stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN
    __autoPy.sendToDefaultMouse(stroke)
    utils.minSleep()
    __autoPy.moveMouseToPosition(point[0], point[1] + 295)
    stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_UP
    __autoPy.sendToDefaultMouse(stroke)
    utils.sleep()

def __openCaptchaWindow(point):
    global __autoPy
    global __chatButtonTemplate
    chatPoint = utils.detectTemplatePivot(utils.grabImage(), __chatButtonTemplate, 0.6, (0.5, 0.5))
    if not chatPoint:
        return False
    __autoPy.moveMouseToPosition(chatPoint[0], chatPoint[1])
    utils.leftClick(__autoPy)
    utils.sleep()
    return True
 
def __macros():
    global __chatScrollTemplate
    global __autoPy

    __openChatWindow()
    scrollCenterPoint = utils.detectTemplatePivot(utils.grabImage(), __chatScrollTemplate, 0.8, (0.5, 0.5))
    if not scrollCenterPoint:
        print('No scrollCenterPoint')
        return

    __scrollChatWindow(scrollCenterPoint)
    openCaptchaResult = __openCaptchaWindow(scrollCenterPoint)
    if not openCaptchaResult:
        print('No openCaptchaResult')
        return

    captchaResult = captchaHelper.proceedCaptcha(__autoPy)
    if not captchaResult:
        print('No captchaResult')
        return

    manorResult = manorHelper.processManor(__autoPy)
    if not manorResult:
        return

def proceed(autohotpy, event):
    global __paused
    utils.updateConfig()
    __macros()
    
    utils.minSleep()
    autohotpy.ESC.press()
    utils.minSleep()
    autohotpy.ESC.press()
    utils.minSleep()
    autohotpy.ESC.press()
    utils.minSleep()

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
    utils.updateConfig()
    __autoPy.registerForKeyDown(__autoPy.F11, __switchPause)
    __autoPy.registerExit(__autoPy.ESC, __onExit)
    __autoPy.start()
    

def main():
    run()

if __name__ == '__main__':
    main()

