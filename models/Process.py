import cv2
from models.TesseractOCR import TesseractOCR
from models.Text2Braille import Text2Braille
from models.KmeansPreProcessing import K_means_cluster

class Process:
    def __init__(self, path):
        self.path = path

    def process(self):
        path = self.path
        image = cv2.imread(path)
        preprocessing_image = K_means_cluster(image).cluster()
        text = TesseractOCR(preprocessing_image).extractText()

        # braille = Text2Braille(post_processing_text).text_to_braille()
        return text
