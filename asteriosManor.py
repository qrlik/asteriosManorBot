from lib.AutoHotPy import AutoHotPy
from lib.InterceptionWrapper import InterceptionMouseState, InterceptionMouseStroke
import cv2  # openCV
import utils
import time
import captchaHelper

__autoPy = AutoHotPy()
__chatScrollTemplate = cv2.imread("assets/chatScroll.png", cv2.IMREAD_GRAYSCALE)
__config = None
__delay = 0.0
__paused = True
    
def __updateConfig():
    global __config
    __config = utils.loadJsonFile('config')

def __init():
    global __config
    global __delay
    __updateConfig()
    __delay = __config['delay']
    utils.init(__config)

def __openChatWindow():
    global __autoPy
    global __delay
    __autoPy.F1.press()
    __autoPy.F1.press()
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
 
def __macros():
    global __chatScrollTemplate
    global __delay
    #'shift' hold

    #__openChatWindow()
    #scrollCenterPoint = utils.detectTemplatePivot(utils.grabImage(), __chatScrollTemplate, 0.8, (0.5, 0.5))
    #if not scrollCenterPoint:
    #    return
    #__scrollChatWindow(scrollCenterPoint)
    #__openCaptchaWindow(scrollCenterPoint)
    captchaResult = captchaHelper.proceedCaptcha()
    if not captchaResult:
        return

    #'shift' up
    time.sleep(__delay)


def proceed(autohotpy, event):
    global __paused
    __updateConfig()
    __macros()
    #few 'esc'
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
    #__autoPy.start()
    __macros()

    

def main():
    run()

    #__init() # debug
    #proceed(None, None)

if __name__ == '__main__':
    main()

