import os
import random
import shutil

def move_and_rename_images(source_folder, dest_folder):
    # Lấy danh sách tất cả các tệp tin trong thư mục nguồn
    source_files = os.listdir(source_folder)

    # Chọn ngẫu nhiên 1000 tệp tin từ danh sách
    selected_files = random.sample(source_files, 1000)

    # Tạo thư mục đích nếu chưa tồn tại
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # Biến đếm để theo dõi số lượng tệp tin đã được xử lý
    count = 1

    # Di chuyển và đổi tên các tệp tin
    for filename in selected_files:
        source_path = os.path.join(source_folder, filename)
        dest_path = os.path.join(dest_folder, f"img{count}.jpg")

        # Di chuyển và đổi tên tệp tin
        shutil.move(source_path, dest_path)
        print(f"Moved and renamed: {filename} -> img{count}.jpg")

        # Tăng biến đếm
        count += 1

# Thư mục nguồn chứa ảnh gốc
source_folder = "D:\\STUDY\\DHSP\\Year3\\HK1\\DigitalImageProcessing-ThayVietDzeThuong\\Final-Project\\Dataset\\train-0\\publaynet\\val"

# Thư mục đích để chuyển ảnh và đổi tên
destination_folder = "D:\\STUDY\\DHSP\\Year3\\HK1\\DigitalImageProcessing-ThayVietDzeThuong\\Final-Project\\Dataset\\train-0\\publaynet\\DocSeg"

# Gọi hàm để thực hiện chuyển và đổi tên ảnh
move_and_rename_images(source_folder, destination_folder)
