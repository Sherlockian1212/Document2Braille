import cv2
from KmeansPreProcessing import K_means_cluster
from TesseractOCR import TesseractOCR
from Text2Braille import Text2Braille
from PostProcessingText import PostProcessingText


def process(path):
    image = cv2.imread(path)
    preprocessing_image = K_means_cluster(image).cluster()
    text = TesseractOCR(preprocessing_image).extractText()
    post_processing_text = PostProcessingText(text).post_processing()
    braille = Text2Braille(post_processing_text).text_to_braille()
    return braille
