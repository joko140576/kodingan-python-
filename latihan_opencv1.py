import cv2

# Inisialisasi capture webcam
cap = cv2.VideoCapture(0)

# Periksa apakah webcam berhasil dibuka
if not cap.isOpened():
    print("Error: Tidak dapat membuka aliran video.")
    exit()

while True:
    # Tangkap frame per frame
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Gagal menangkap gambar.")
        break
    
    # Tampilkan frame yang dihasilkan
    cv2.imshow('Webcam Capture', frame)

    # Keluar dari jendela webcam saat tombol 'q' ditekan
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Lepaskan webcam dan tutup jendela
cap.release()
cv2.destroyAllWindows()
