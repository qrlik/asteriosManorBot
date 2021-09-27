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
    
    def __onPress(self, key):
        if key == keyboard.Key.pause or key == keyboard.Key.end:
            self.__paused = not self.__paused

    def __init__(self, *args, **kwargs):
        self.__keyboardListener = keyboard.Listener(on_press=self.__onPress)
        self.__keyboardListener.start()
        self.__config = utils.loadJsonFile('config')
        self.__monitor['top'] = int(self.__config['resolutionHeight'] / 5)
        self.__monitor['height'] = int(self.__config['resolutionHeight'] / 5 * 3)
        self.__monitor['left'] = 0
        self.__monitor['width'] = int(self.__config['resolutionWidth'] / 4 * 3)
        
    async def __checkPause(self):
        while self.__paused:
            await asyncio.sleep(3)
        return

    async def __openFirstWindow(self):
        await self.__checkPause()
        pyautogui.press(self.__config['targetButton'])

    async def __detectFirstWindow(self):
        with mss.mss() as screenshotManager:
            while "searching first window":
                await self.__checkPause()
                img = numpy.array(screenshotManager.grab(self.__monitor))

                cv2.imshow("test", img)
                key = cv2.waitKey(1)

                #processedImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    async def run(self):
        while True:
            #with pyautogui.hold('shift'):
                await self.__openFirstWindow()
                await self.__detectFirstWindow()


async def main():
    while True:
        #try:
            mainSystem = manorSystem()
            await mainSystem.run()
        #except Exception as e:
        #    print('main: error: ' + str(e))


if __name__ == '__main__':
    asyncio.run(main())

