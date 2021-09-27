from pynput import keyboard  # слушатель ввода
import numpy  # поддержка многомерных массивов | поддержка высокоуровневых математических функций
import cv2  # openCV
import mss  # создания скриншотов
import pyautogui  # действия с клавиатурой и с мышкой
import utils
import asyncio

class manorSystem:
    __config = {}
    __paused = True
    __monitor = {"top": 0, "left": 0, "width": 0, "height": 0}
    __keyboardListener = None
    __chatWindowTemplate = None
    
    def __onPress(self, key):
        if key == keyboard.Key.pause or key == keyboard.Key.end:
            self.__paused = not self.__paused

    def __init__(self, *args, **kwargs):
        self.__keyboardListener = keyboard.Listener(on_press=self.__onPress)
        self.__keyboardListener.start()
        self.__chatWindowTemplate = cv2.imread("assets/chatScroll.png", cv2.IMREAD_GRAYSCALE)
        self.__config = utils.loadJsonFile('config')
        self.__monitor['top'] = int(self.__config['resolutionHeight'] / 5)
        self.__monitor['height'] = int(self.__config['resolutionHeight'] / 5 * 3)
        self.__monitor['left'] = 0
        self.__monitor['width'] = int(self.__config['resolutionWidth'] / 4 * 3)
        
    async def __checkPause(self):
        while self.__paused:
            await asyncio.sleep(3)
        return

    async def __openChatWindow(self):
        await self.__checkPause()
        pyautogui.press(self.__config['targetButton'])

    async def __detectChatWindowScroll(self):
        with mss.mss() as screenshotManager:
            while "searching chat window":
                await self.__checkPause()
                img = numpy.array(screenshotManager.grab(self.__monitor))
                processedImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                res = cv2.matchTemplate(processedImage, self.__chatWindowTemplate, cv2.TM_CCOEFF_NORMED)
                loc = numpy.where(res >= 0.7)

                height = self.__chatWindowTemplate.shape[0]
                width = self.__chatWindowTemplate.shape[1]
                for point in zip(*loc[::-1]):
                    cv2.rectangle(img, point, (point[0] + width, point[1] + height), (0, 255, 0), 3)

                cv2.imshow("test", img)
                key = cv2.waitKey(1)

    async def run(self):
        while True:
            #with pyautogui.hold('shift'):
                await self.__openChatWindow()
                await self.__detectChatWindowScroll()


async def main():
    while True:
        #try:
            mainSystem = manorSystem()
            await mainSystem.run()
        #except Exception as e:
        #    print('main: error: ' + str(e))


if __name__ == '__main__':
    asyncio.run(main())

