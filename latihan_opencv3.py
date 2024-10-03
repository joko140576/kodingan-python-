import cv2

def load_haarcascades():
    # Memuat model Haar Cascade untuk deteksi wajah, mata, hidung, dan mulut
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    nose_cascade = cv2.CascadeClassifier('haarcascade_mcs_nose.xml')
    mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')
    return face_cascade, eye_cascade, nose_cascade, mouth_cascade

def detect_features(frame, face_cascade, eye_cascade, nose_cascade, mouth_cascade):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Deteksi wajah
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        # Deteksi mata
        eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=10)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
            cv2.putText(frame, "Mata", (x + ex, y + ey - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Deteksi hidung
        noses = nose_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=10)
        nose_detected = False  # Flag untuk menandakan apakah hidung terdeteksi
        for (nx, ny, nw, nh) in noses:
            cv2.rectangle(roi_color, (nx, ny), (nx + nw, ny + nh), (255, 0, 255), 2)
            cv2.putText(frame, "Hidung", (x + nx, y + ny - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
            nose_detected = True  # Hidung terdeteksi

        # Deteksi mulut
        mouths = mouth_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=10)
        for (mx, my, mw, mh) in mouths:
            # Pastikan mulut terdeteksi di bawah hidung
            if nose_detected and my > ny + nh:  # Cek jika mulut berada di bawah hidung
                cv2.rectangle(roi_color, (mx, my), (mx + mw, my + mh), (0, 0, 255), 2)
                cv2.putText(frame, "Mulut", (x + mx, y + my - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    return frame

def main():
    face_cascade, eye_cascade, nose_cascade, mouth_cascade = load_haarcascades()
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera not accessible.")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break

        # Deteksi fitur wajah
        frame = detect_features(frame, face_cascade, eye_cascade, nose_cascade, mouth_cascade)

        # Menampilkan video
        cv2.imshow('Face, Eye, Nose and Mouth Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
