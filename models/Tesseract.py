import pytesseract
import cv2

class Tesseract:
    def __init__(self, image):
        self.image = image
    def extractText(self):
        image = self.image

        # dir = 'D:\\STUDY\\DHSP\\Year3\\HK1\\DigitalImageProcessing-ThayVietDzeThuong\\Final-Project\\Document2Braille\\resources\\Tesseract\\'

        # Convert to gray color
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # cv2.imwrite(dir + f"gray.png", gray)
        # cv2.imshow("gray", gray)
        # cv2.waitKey(0)

        #Adjust contrast
        alpha = 1.5
        beta = 0
        contrast_adjusted_image = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)
        # cv2.imwrite(dir + f"contrast_adjusted_image.png", contrast_adjusted_image)
        # cv2.imshow("contrast_adjusted_image", contrast_adjusted_image)
        # cv2.waitKey(0)

        text = pytesseract.image_to_string(contrast_adjusted_image, lang='vie')

        file_path = 'D:\\STUDY\\DHSP\\Year3\\HK1\\DigitalImageProcessing-ThayVietDzeThuong\\Final-Project\\Document2Braille\\output\\output.txt'

        # Mở file để ghi (mode='w' là chế độ ghi)
        with open(file_path, 'w', encoding='utf-8') as file:
            # Ghi chuỗi vào file
            file.write(text)

        return text

# img = cv2.imread('D:\\STUDY\\DHSP\\Year3\\HK1\\DigitalImageProcessing-ThayVietDzeThuong\\Final-Project\\Document2Braille\\resources\\K-means\\final.png')
# ex_text = Tesseract(img).extractText()
# print(ex_text)