from pynput import keyboard  # слушатель ввода
import numpy  # поддержка многомерных массивов | поддержка высокоуровневых математических функций
import cv2  # openCV
import mss  # создания скриншотов
import utils
import time

class manorSystem:
    __config = {}
    __delay = None
    __paused = True
    __monitor = {"top": 0, "left": 0, "width": 0, "height": 0}
    __keyboardListener = None
    __chatWindowTemplate = None
    
    def __onPress(self, key):
        if key == keyboard.Key.pause or key == keyboard.Key.end:
            self.__paused = not self.__paused
            print('Paused' if self.__paused else 'Resumed')

    def __init__(self, *args, **kwargs):
        self.__keyboardListener = keyboard.Listener(on_press=self.__onPress)
        self.__keyboardListener.start()
        self.__chatWindowTemplate = cv2.imread("assets/chatScroll.png", cv2.IMREAD_GRAYSCALE)
        self.__config = utils.loadJsonFile('config')
        self.__delay = self.__config['delay']
        self.__monitor['top'] = int(self.__config['resolutionHeight'] / 5)
        self.__monitor['height'] = int(self.__config['resolutionHeight'] / 5 * 3)
        self.__monitor['left'] = 0
        self.__monitor['width'] = int(self.__config['resolutionWidth'] / 4 * 3)
        
    def __getGlobalPoint(self, x, y):
        return (x + self.__monitor['left'], y + self.__monitor['top'])

    def __checkPause(self):
        while self.__paused:
            time.sleep(3)
        return

    def __openChatWindow(self):
        self.__checkPause()
        #pyautogui.press(self.__config['targetButton'], 2, self.__delay)

    def __detectChatWindowScroll(self):
        with mss.mss() as screenshotManager:
            while True:
                self.__checkPause()
                img = numpy.array(screenshotManager.grab(self.__monitor))
                processedImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                res = cv2.matchTemplate(processedImage, self.__chatWindowTemplate, cv2.TM_CCOEFF_NORMED)
                loc = numpy.where(res >= 0.9)

                for point in zip(*loc[::-1]):
                    templateHeight = self.__chatWindowTemplate.shape[0]
                    templateWidth = self.__chatWindowTemplate.shape[1]

                    #cv2.rectangle(img, point, (point[0] + templateWidth, point[1] + templateHeight), (0, 255, 0), 3)
                    #cv2.imshow("test", img)
                    #key = cv2.waitKey(1)
                    
                    scrollPoint = self.__getGlobalPoint(point[0], point[1])
                    scrollMiddlePoint = (int(scrollPoint[0] + templateWidth / 2), int(scrollPoint[1] + templateHeight / 2))
                    return scrollMiddlePoint
                time.sleep(self.__delay)

    def __scrollChatWindow(self, point):
        self.__checkPause()
        #pyautogui.moveTo(point[0], point[1], self.__delay)
        #pyautogui.mouseDown()
        #pyautogui.move(0, 295, self.__delay)
        #pyautogui.mouseUp()
        time.sleep(self.__delay)
        #pyautogui.drag(0, 295, self.__delay, button = 'left')

    def run(self):
        while True:
            #with pyautogui.hold('shift'):
                self.__openChatWindow()
                scrollPoint = self.__detectChatWindowScroll()
                self.__scrollChatWindow(scrollPoint)


def main():
    while True:
        #try:
            mainSystem = manorSystem()
            mainSystem.run()
        #except Exception as e:
        #    print('main: error: ' + str(e))


if __name__ == '__main__':
    main()

