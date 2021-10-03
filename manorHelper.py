from lib.AutoHotPy import AutoHotPy
from lib.InterceptionWrapper import InterceptionMouseState, InterceptionMouseStroke
import utils
import cv2

__editSalesTemplate = cv2.imread("assets/editSales.png", cv2.IMREAD_GRAYSCALE)
__maxPriceTemplate = cv2.imread("assets/maxPrice.png", cv2.IMREAD_GRAYSCALE)
__posDict = {}

def __openSeedMenu(autohotpy, index, editPoint):
    seedY = editPoint[1] - (224 - index * 18)
    autohotpy.moveMouseToPosition(editPoint[0], seedY)
    utils.minSleep()
    utils.leftClick(autohotpy) # seed choise
    utils.minSleep()
    autohotpy.moveMouseToPosition(editPoint[0], editPoint[1])
    utils.minSleep()
    utils.leftClick(autohotpy) # open seed menu
    utils.sleep()

def __setupSeed(autohotpy, town):
    global __maxPriceTemplate
    maxPricePoint = utils.detectTemplatePivot(utils.grabImage(), __maxPriceTemplate, 0.8, (0.5, 0.5))
    if not maxPricePoint:
        return False
    arrowPoint = (maxPricePoint[0] + 27, maxPricePoint[1] - 23)
    autohotpy.moveMouseToPosition(arrowPoint[0], arrowPoint[1])
    utils.minSleep()
    utils.leftClick(autohotpy) # open towns list
    utils.minSleep()
    autohotpy.moveMouseToPosition(arrowPoint[0], arrowPoint[1] + 36 + 17 * town)
    utils.minSleep()
    utils.leftClick(autohotpy) # choose town
    utils.minSleep()
    autohotpy.moveMouseToPosition(maxPricePoint[0] - 75, maxPricePoint[1])
    utils.minSleep()
    utils.leftClick(autohotpy) # focus count edit
    utils.minSleep()
    autohotpy.N0.press() # enter seed count
    utils.minSleep()
    autohotpy.moveMouseToPosition(maxPricePoint[0] - 100, maxPricePoint[1] + 35)
    utils.minSleep()
    utils.leftClick(autohotpy) # accept seed
    utils.minSleep()
    return True

def processManor(autohotpy):
    global __editSalesTemplate
    editSalesPoint = utils.detectTemplatePivot(utils.grabImage(), __editSalesTemplate, 0.8, (0.5, 0.5))
    if not editSalesPoint:
        return False
    index = 2
    __openSeedMenu(autohotpy, index, editSalesPoint)
    town = 5
    setupSeedResult = __setupSeed(autohotpy, town)
    if not setupSeedResult:
        return False
    autohotpy.moveMouseToPosition(editSalesPoint[0] + 415, editSalesPoint[1])
    utils.minSleep()
    utils.leftClick(autohotpy) # accept manor
    return True