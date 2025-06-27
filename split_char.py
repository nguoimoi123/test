import cv2
import os
import numpy as np
from glob import glob

output_dir = "char_dataset"
os.makedirs(output_dir, exist_ok=True)

# Lấy danh sách tất cả file train*.png
image_paths = sorted(glob("training14.png"))

if not image_paths:
    print("Không tìm thấy ảnh train4.png")
    exit()
char_count = {}
image_files = []
labels = []
print(f"Đã tìm thấy {len(image_paths)} ảnh. Bắt đầu tách ký tự...")
print("Gõ nhãn tương ứng cho mỗi ký tự hiển thị (A-Z, 0-9, hoặc '-')")

for image_path in image_paths:
    print(f"\nĐang xử lý ảnh: {image_path}")
    image = cv2.imread(image_path)
    if image is None:
        print(f"Không đọc được ảnh {image_path}")
        continue
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bounding_boxes = [cv2.boundingRect(c) for c in contours]
    sorted_boxes = sorted(bounding_boxes, key=lambda x: x[0])

    for i, (x, y, w, h) in enumerate(sorted_boxes):
        if w < 5 or h < 10:
            continue

        roi = thresh[y:y+h, x:x+w]
        roi_resized = cv2.resize(roi, (40, 40))

        cv2.imshow("Ký tự cần gán nhãn", roi_resized)
        print("Gõ nhãn cho ký tự (A-Z, 0-9, hoặc '-'):")
        key = cv2.waitKey(0)

        if key == 27:  # ESC
            print("Thoát gán nhãn.")
            cv2.destroyAllWindows()
            exit()

        label = chr(key).upper()
        if not (label.isalnum() or label in "-."):
            print("Nhãn không hợp lệ, bỏ qua.")
            continue

        label_dir = os.path.join(output_dir, label)
        os.makedirs(label_dir, exist_ok=True)
        count = char_count.get(label, 0)
        filename = os.path.join(label_dir, f"{label}_{count}.png")
        cv2.imwrite(filename, roi_resized)
        
        labels.append(label)
        image_files.append(filename)

        print(f"Đã lưu: {filename}")
        char_count[label] = count + 1
        print(f"Đã lưu: {filename}")
        char_count[label] = count + 1
cv2.destroyAllWindows()
with open(os.path.join(output_dir, "labels.txt"), "w", encoding="utf-8") as f:
    for label in labels:
        f.write(label + "\n")
print("\nĐã hoàn tất tách ký tự từ tất cả các ảnh train4.png.")
