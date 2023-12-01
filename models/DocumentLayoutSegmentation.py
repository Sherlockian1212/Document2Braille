import cv2


class DocumentLayoutSegmentation:
    def __init__(self, image):
        self.image = image

    def segmentation(self):

        # Load image, grayscale, Gaussian blur, Otsu's threshold
        #D'D:\\STUDY\\DHSP\\Year3\\HK1\\DigitalImageProcessing-ThayVietDzeThuong\\Final-Project\\Document2Braille\\uploads\\SGK06.png')
        image = self.image
        dim_limit = 1080
        max_dim = max(image.shape)
        if max_dim > dim_limit:
            resize_scale = dim_limit / max_dim
            image = cv2.resize(image, None, fx=resize_scale, fy=resize_scale)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (7,7), 0)

        # cv2.imshow("blur", blur)
        # cv2.waitKey(0)

        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # cv2.imshow("thresh", thresh)
        # cv2.waitKey(0)


        # Create rectangular structuring element and dilate
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
        dilate = cv2.dilate(thresh, kernel, iterations=4)
        # cv2.imshow("dilate", thresh)
        # cv2.waitKey(0)

        # Find contours and draw rectangle
        cnts = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        height, width, _ = image.shape
        min_contour_area = (width * height) / 80
        max_contour_area = (width * height) * 9 / 10

        filtered_cnts = [cnt for cnt in cnts if min_contour_area <= cv2.contourArea(cnt) <= max_contour_area]

        filtered_cnts = sorted(filtered_cnts, key=lambda cnt: cv2.boundingRect(cnt)[1])

        dir = 'D:\\STUDY\\DHSP\\Year3\\HK1\\DigitalImageProcessing-ThayVietDzeThuong\\Final-Project\\Document2Braille\\output\\'
        # Duyệt qua từng đường viền và cắt hình ảnh thành các phần nhỏ
        for i, cnt in enumerate(filtered_cnts):
            # Tính toán hộp giới hạn của đường viền
            x, y, w, h = cv2.boundingRect(cnt)

            # Cắt hình ảnh theo hộp giới hạn
            roi = image[y:y + h, x:x + w]

            # Lưu hình ảnh cắt được (có thể lưu vào thư mục khác nhau)
            cv2.imwrite(dir + f"cropped_image_{i+1}.png", roi)

        for c in filtered_cnts:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)

        # cv2.imwrite(dir + f"segmentation.png", image)
        # cv2.imshow("segmentation", image)
        # cv2.waitKey(0)
        return image

# img = cv2.imread("D:\\STUDY\\DHSP\\Year3\\HK1\\DigitalImageProcessing-ThayVietDzeThuong\\Final-Project\\Document2Braille\\output\\edgedetection.png")
# result = DocumentLayoutSegmentation(img).segmentation()