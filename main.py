import cv2
from PIL import Image
from models import EdgeDetection, DocumentLayoutSegmentation
import pytesseract
import os
import glob

def preProcess(path):
    image = cv2.imread(path)
    preprocessing = EdgeDetection.imagePreprocessing(image)
    preprocessing_image = preprocessing.imageProcessing()
    layout_segmentation = DocumentLayoutSegmentation.DocumentLayoutSegmentation(preprocessing_image)
    layout_segmentation.segmentation()
def extractText(image):
    # Chuyển ảnh sang độ xám
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Xử lý ảnh (tuỳ chọn)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # Ghi tạm ảnh xuống ổ cứng để sau đó apply OCR
    temp_filename = "temp.png"
    cv2.imwrite(temp_filename, gray)

    # Load ảnh và apply nhận dạng bằng Tesseract OCR
    text = pytesseract.image_to_string(Image.open(temp_filename), lang='vie')

    # Xóa ảnh tạm sau khi nhận dạng
    os.remove(temp_filename)

    return text

def save_txt(text):
    # Tên file và đường dẫn
    file_path = 'D:\\STUDY\\DHSP\\Year3\\HK1\\DigitalImageProcessing-ThayVietDzeThuong\\Final-Project\\Document2Braille\\output\\output.txt'

    # Mở file để ghi (mode='w' là chế độ ghi)
    with open(file_path, 'w', encoding='utf-8') as file:
        # Ghi chuỗi vào file
        file.write(text)

    print("Chuỗi đã được lưu vào file thành công.")

if __name__ == '__main__':
    path = 'D:\\STUDY\\DHSP\\Year3\\HK1\\DigitalImageProcessing-ThayVietDzeThuong\\Final-Project\\Document2Braille\\uploads\\test01.jpg'
    preProcess(path=path)

    # Đường dẫn đến thư mục chứa hình ảnh
    folder_path = 'D:\\STUDY\\DHSP\\Year3\\HK1\\DigitalImageProcessing-ThayVietDzeThuong\\Final-Project\\Document2Braille\\output'

    # Định dạng hình ảnh bạn quan tâm (ví dụ: *.jpg, *.png)
    image_format = "*.png"

    # Kết hợp đường dẫn thư mục và định dạng để tạo đường dẫn đầy đủ
    search_pattern = os.path.join(folder_path, image_format)

    text = ''
    # Duyệt qua từng hình ảnh
    for image_path in glob.glob(search_pattern):
        image = cv2.imread(image_path)
        text = text + extractText(image) + '\n'
        
    save_txt(text)

