import cv2
from PIL import Image
from models import Kmeans
from models import Tesseract
import pytesseract
import os
import glob

def preProcess(path):
    image = cv2.imread(path)
    preprocessing = Kmeans.K_means(image)
    preprocessing_image = preprocessing.cluster()
    return preprocessing_image

if __name__ == '__main__':
    path = 'D:\\STUDY\\DHSP\\Year3\\HK1\\DigitalImageProcessing-ThayVietDzeThuong\\Final-Project\\Document2Braille\\uploads\\test (29).jpg'
    pre_processing_img = preProcess(path=path)
    ex_text = Tesseract(pre_processing_img).extractText()
    print(ex_text)

