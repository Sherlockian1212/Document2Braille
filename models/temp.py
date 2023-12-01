import cv2
import numpy as np

# Đọc ảnh và chuyển sang ảnh xám
image = cv2.imread('D:\\STUDY\\DHSP\\Year3\\HK1\\DigitalImageProcessing-ThayVietDzeThuong\\Final-Project\\Document2Braille\\output\\edgedetection.png', cv2.IMREAD_GRAYSCALE)

# Áp dụng thresholding (nếu cần)
_, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)

# Kết nối các thành phần liên thông
num_labels, labeled_image = cv2.connectedComponents(binary_image)

# Tìm và vẽ đường bao lồi cho từng thành phần liên thông
colored_image = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2BGR)

for label in range(1, num_labels):
    # Lấy các điểm của thành phần liên thông
    points = np.column_stack(np.where(labeled_image == label))

    # Tìm đường bao lồi
    hull = cv2.convexHull(points)

    # Vẽ đường bao lồi lên ảnh
    cv2.drawContours(colored_image, [hull], -1, (0, 255, 0), 2)

# Hiển thị ảnh gốc và ảnh có đường bao lồi
# cv2.imshow('Original Image', image)
cv2.imshow('Convex Hulls', colored_image)
cv2.waitKey(0)
# cv2.destroyAllWindows()
