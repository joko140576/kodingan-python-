import cv2
from ultralytics import YOLO

# Load model YOLOv8
model = YOLO('C:\\Users\\jokos\\Desktop\\latihan pyton\\training -ai2024\\best.pt')

# Buka kamera atau video
cap = cv2.VideoCapture(0)  # Ganti 0 dengan file video jika menggunakan video file

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Deteksi objek menggunakan model YOLO
    results = model(frame)  # Deteksi langsung pada frame

    # Visualisasi deteksi di frame
    annotated_frame = results[0].plot()  # Annotasi hasil deteksi ke frame

    # Tampilkan hasil deteksi
    cv2.imshow("YOLOv8 Object Detection", annotated_frame)

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Bersihkan semua
cap.release()
cv2.destroyAllWindows()
