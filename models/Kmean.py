import numpy as np
import cv2
import matplotlib.image as img
from sklearn.cluster import KMeans
from collections import Counter

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

img = img.imread('D:\\STUDY\\DHSP\\Year3\\HK1\\DigitalImageProcessing-ThayVietDzeThuong\\Final-Project\\Document2Braille\\uploads\\test19.jpg')

class Kmean:
    def __init__(self, image):
        self.image = image
    def cluster(self):
        img = self.image
        dim_limit = 1080
        max_dim = max(img.shape)
        if max_dim > dim_limit:
            resize_scale = dim_limit / max_dim
            img = cv2.resize(img, None, fx=resize_scale, fy=resize_scale)

        # Create a copy of resized original image for later use
        orig_img = img.copy()
        # cv2.imshow("original_resized", orig_img)

        # Repeated Closing operation to remove text from the document.
        kernel = np.ones((9, 9), np.uint8)
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=3)
        cv2.imshow('morphology', img)
        cv2.waitKey(0)

        (h,w,c) = img.shape
        img2D = img.reshape(h*w,c)

        kmeans_model = KMeans(n_clusters=7)
        cluster_labels = kmeans_model.fit_predict(img2D)

        print(kmeans_model.cluster_centers_)
        rgb_cols = kmeans_model.cluster_centers_.round(0).astype(int)

        labels_count = Counter(cluster_labels)
        print(labels_count)

        img_quant = np.reshape(rgb_cols[cluster_labels],(h,w,c)).astype(np.uint8)
        print('done')
        # cv2.imshow('cluster',img_quant)
        # cv2.waitKey(0)

        # Find the label of the largest cluster
        largest_cluster_label = max(labels_count, key=labels_count.get)

        # Create a mask for the largest cluster
        largest_cluster_mask = (cluster_labels == largest_cluster_label).reshape(h, w)
        cluster_image = (largest_cluster_mask * 255).astype(np.uint8)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        dilate = cv2.dilate(cluster_image, kernel, iterations=4)

        contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        cnt = sorted(contours, key=cv2.contourArea, reverse=True)
        largest_contour = cnt[0]

        result_image = cv2.drawContours(orig_img.copy(), [largest_contour], -1, (0, 255, 0), 2)

        cv2.imshow('cluster_image',result_image)
        cv2.waitKey(0)

        all_points = np.concatenate(largest_contour)
        hull = cv2.convexHull(all_points)

        re = orig_img.copy()
        cv2.drawContours(re, [hull], -1, (0, 255, 0), 2)

        cv2.imshow('hull', re)
        cv2.waitKey(0)

        x, y, w, h = cv2.boundingRect(hull)

        # Cắt ảnh theo hình chữ nhật
        cropped_img = orig_img[y:y + h, x:x + w]

        # dir = 'D:\\STUDY\\DHSP\\Year3\\HK1\\DigitalImageProcessing-ThayVietDzeThuong\\Final-Project\\Document2Braille\\output\\'
        # cv2.imwrite(dir + f"k-mean.png", cropped_img)

        epsilon = 0.02 * cv2.arcLength(hull, True)
        corners = cv2.approxPolyDP(hull, epsilon, True)
        # if our approximated contour has four points
        # if len(corners) == 4:
        #     break
        # Sorting the corners and converting them to desired shape.

        corners = sorted(np.concatenate(corners).tolist())
        # For 4 corner points being detected.
        # Rearranging the order of the corner points.
        corners = order_points(corners)

        image_with_corners = orig_img.copy()
        for corner in corners:
            cv2.circle(image_with_corners, tuple(corner), 5, (0, 255, 0), -1)

        # Hiển thị ảnh với các điểm đã vẽ
        cv2.imshow('Image with Corners', image_with_corners)
        cv2.waitKey(0)

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

        dir = 'D:\\STUDY\\DHSP\\Year3\\HK1\\DigitalImageProcessing-ThayVietDzeThuong\\Final-Project\\Document2Braille\\output\\'
        cv2.imwrite(dir + f"edgedetection.png", final)

k = Kmean(img)
k.cluster()