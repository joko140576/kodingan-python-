import cv2
import dlib

# Muat model deteksi wajah dan landmarks dari dlib
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# Muat gambar kacamata (dengan transparansi)
glasses = cv2.imread('glasses.png', -1)

# Buka kamera
cap = cv2.VideoCapture(0)

while True:
    # Baca frame dari kamera
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Deteksi wajah di frame
    faces = detector(gray)

    for face in faces:
        # Dapatkan landmarks (titik-titik fitur wajah)
        landmarks = predictor(gray, face)

        # Koordinat mata kiri dan mata kanan (landmark 36-41 untuk mata kiri, 42-47 untuk mata kanan)
        left_eye = (landmarks.part(36).x, landmarks.part(36).y)
        right_eye = (landmarks.part(45).x, landmarks.part(45).y)

        # Hitung lebar antara kedua mata
        eye_width = right_eye[0] - left_eye[0]

        # Sesuaikan ukuran kacamata berdasarkan lebar mata
        glasses_resized = cv2.resize(glasses, (int(eye_width * 1.2), int(glasses.shape[0] * (eye_width * 1.2) / glasses.shape[1])))

        # Dapatkan koordinat kiri atas untuk menempatkan kacamata di atas mata
        # Menempatkan kacamata sedikit lebih rendah agar terlihat lebih natural
        top_left = (left_eye[0] - int(glasses_resized.shape[1] / 4), left_eye[1] - int(glasses_resized.shape[0] / 2.5))

        # Buat overlay kacamata pada wajah di frame
        for i in range(glasses_resized.shape[0]):
            for j in range(glasses_resized.shape[1]):
                if glasses_resized[i, j][3] != 0:  # Jika piksel kacamata bukan transparan
                    frame[top_left[1] + i, top_left[0] + j] = glasses_resized[i, j][:3]

    # Tampilkan frame dengan augmentasi kacamataq
    cv2.imshow('Kacamata Augmentasi', frame)

    # Tekan 'q' untuk keluar dari loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Tutup kamera dan jendela
cap.release()
cv2.destroyAllWindows()
