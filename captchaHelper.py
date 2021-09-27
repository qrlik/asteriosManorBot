
import pytesseract
import cv2
from PIL import Image

if __name__ == '__main__':
    #pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\tesseract.exe'
    image = cv2.imread("assets/captchaTest.png")
    text = pytesseract.image_to_string(image)
    print(text)