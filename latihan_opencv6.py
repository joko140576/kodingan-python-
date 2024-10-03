import cv2
import numpy as np
from collections import Counter

def get_dominant_color(image, k=1):
    pixels = np.float32(image.reshape(-1, 3))
    n_colors = k
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    counts = Counter(labels.flatten())
    dominant = palette[np.argmax(counts)]
    return dominant

# Baca gambar acuan untuk 100 ribu dan 50 ribu
image_100k_ref = cv2.imread(r'C:\Users\jokos\Desktop\latihan pyton\training -ai2024\uang_100k.jpg')
if image_100k_ref is None:
    print("Gambar uang 100 ribu tidak dapat dibaca. Periksa path dan file.")

image_50k_ref = cv2.imread(r'C:\Users\jokos\Desktop\latihan pyton\training -ai2024\uang_50k.jpg')
if image_50k_ref is None:
    print("Gambar uang 50 ribu tidak dapat dibaca. Periksa path dan file.")

# Ubah ukuran gambar acuan hanya jika gambar berhasil dibaca
if image_100k_ref is not None:
    image_100k_ref_resized = cv2.resize(image_100k_ref, (100, 100))

if image_50k_ref is not None:
    image_50k_ref_resized = cv2.resize(image_50k_ref, (100, 100))

# Inisialisasi kamera
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        print("Gagal mengambil frame dari kamera.")
        break

    # Ubah ukuran frame
    frame_resized = cv2.resize(frame, (100, 100))

    # Dapatkan warna dominan dari frame hanya jika gambar acuan berhasil dibaca
    if image_100k_ref is not None:
        dominant_color_100k_ref = get_dominant_color(image_100k_ref_resized)
    
    if image_50k_ref is not None:
        dominant_color_50k_ref = get_dominant_color(image_50k_ref_resized)

    # Dapatkan warna dominan dari frame
    dominant_color_frame = get_dominant_color(frame_resized)

    # Bandingkan warna dominan dari frame dengan warna acuan
    if image_100k_ref is not None and np.allclose(dominant_color_frame, dominant_color_100k_ref, atol=50):
        print("Uang 100 ribu terdeteksi!")
    elif image_50k_ref is not None and np.allclose(dominant_color_frame, dominant_color_50k_ref, atol=50):
        print("Uang 50 ribu terdeteksi!")
    else:
        print("Uang tidak terdeteksi atau bukan pecahan yang dikenali.")

    # Tampilkan frame
    cv2.imshow('Kamera', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
