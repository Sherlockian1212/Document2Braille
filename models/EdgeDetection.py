import cv2
import numpy as np

def order_points(pts):
    """Rearrange coordinates to order:
       top-left, top-right, bottom-right, bottom-left"""
    rect = np.zeros((4, 2), dtype='float32')
    pts = np.array(pts)
    s = pts.sum(axis=1)
    # Top-left point will have the smallest sum.
    rect[0] = pts[np.argmin(s)]
    # Bottom-right point will have the largest sum.
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    # Top-right point will have the smallest difference.
    rect[1] = pts[np.argmin(diff)]
    # Bottom-left will have the largest difference.
    rect[3] = pts[np.argmax(diff)]
    # return the ordered coordinates
    return rect.astype('int').tolist()

class imagePreprocessing:
    def __init__(self, image):
        self.image = image

    def imageProcessing(selt):
        img = selt.image

        # Resize image to workable size
        dim_limit = 1080
        max_dim = max(img.shape)
        if max_dim > dim_limit:
            resize_scale = dim_limit / max_dim
            img = cv2.resize(img, None, fx=resize_scale, fy=resize_scale)

        # Create a copy of resized original image for later use
        orig_img = img.copy()

        dir = '/resources/EdgeDetection\\'

        # Repeated Closing operation to remove text from the document.
        kernel = np.ones((9, 9), np.uint8)
        morph = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=3)
        # cv2.imwrite(dir + f"morph.png", morph)
        # cv2.imshow('morphology', morph)
        # cv2.waitKey(0)

        # Binary thresholding
        gray_image = cv2.cvtColor(morph, cv2.COLOR_RGB2GRAY)
        thresh = cv2.adaptiveThreshold(gray_image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,17,2)
        # cv2.imwrite(dir + f"thresh.png", thresh)
        # cv2.imshow('Threshold', thresh)
        # cv2.waitKey(0)

        # Canny
        canny = cv2.Canny(thresh, 0, 200)
        canny = cv2.dilate(canny, cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7)))
        # cv2.imwrite(dir + f"canny.png", canny)
        # cv2.imshow('canny', canny)
        # cv2.waitKey(0)

        # Finding contours for the detected edges.
        contours, hierarchy = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        # Keeping only the largest detected contour.
        cnt = sorted(contours, key=cv2.contourArea, reverse=True)
        largest_contour = cnt[0]
        all_points = np.concatenate(largest_contour)
        hull = cv2.convexHull(all_points)
        hull_img = orig_img.copy()
        cv2.drawContours(hull_img, [hull], -1, (0, 255, 0), 2)
        # cv2.imwrite(dir + f"hull_img.png", hull_img)
        # cv2.imshow('hull', hull_img)
        # cv2.waitKey(0)

        # approximate the contour
        epsilon = 0.02 * cv2.arcLength(hull, True)
        corners = cv2.approxPolyDP(hull, epsilon, True)
        corners = sorted(np.concatenate(corners).tolist())
        corners = order_points(corners)
        corners_img = orig_img.copy()
        for corner in corners:
            cv2.circle(corners_img, tuple(corner), 15, (0, 255, 0), -1)
        # cv2.imwrite(dir + f"corners_img.png", corners_img)
        # cv2.imshow('corners_img', corners_img)
        # cv2.waitKey(0)

        # Finding Destination Co-ordinates
        w1 = np.sqrt((corners[0][0] - corners[1][0]) ** 2 + (corners[0][1] - corners[1][1]) ** 2)
        w2 = np.sqrt((corners[2][0] - corners[3][0]) ** 2 + (corners[2][1] - corners[3][1]) ** 2)
        # Finding the maximum width.
        w = max(int(w1), int(w2))

        h1 = np.sqrt((corners[0][0] - corners[2][0]) ** 2 + (corners[0][1] - corners[2][1]) ** 2)
        h2 = np.sqrt((corners[1][0] - corners[3][0]) ** 2 + (corners[1][1] - corners[3][1]) ** 2)
        # Finding the maximum height.
        h = max(int(h1), int(h2))

        # Final destination co-ordinates.
        destination_corners = order_points(np.array([[0, 0], [w - 1, 0], [0, h - 1], [w - 1, h - 1]]))

        h, w = orig_img.shape[:2]
        # Getting the homography.
        homography, mask = cv2.findHomography(np.float32(corners), np.float32(destination_corners), method=cv2.RANSAC,
                                              ransacReprojThreshold=3.0)
        # Perspective transform using homography.
        un_warped = cv2.warpPerspective(orig_img, np.float32(homography), (w, h), flags=cv2.INTER_LINEAR)
        # Crop
        final = un_warped[:destination_corners[2][1], :destination_corners[2][0]]

        if (final.shape[0] * final.shape[1]) < (orig_img.shape[0] * orig_img.shape[1] / 10):
            final = orig_img

        #dir = 'D:\\STUDY\\DHSP\\Year3\\HK1\\DigitalImageProcessing-ThayVietDzeThuong\\Final-Project\\Document2Braille\\output\\'
        # cv2.imwrite(dir + f"final.png", final)

        return final

# img = cv2.imread('D:\\STUDY\\DHSP\\Year3\\HK1\\DigitalImageProcessing-ThayVietDzeThuong\\Final-Project\\Document2Braille\\uploads\\test (29).jpg')
# k = imagePreprocessing(img)
# k.imageProcessing()