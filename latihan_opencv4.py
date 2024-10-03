import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime

# Fungsi untuk merekam absensi, membuat sendiri file attendance .CSV
def mark_attendance(name):
    file_path = r'C:\Users\jokos\Desktop\latihan pyton\training -ai2024\Absen\attendance.csv'
    file_exists = os.path.isfile(file_path)

    with open(file_path, 'a') as f:
        
        if not file_exists:
            f.write('Name,Date\n')  # Menulis header jika file belum ada
        now = datetime.now()  # Mendapatkan waktu terkini
        dtString = now.strftime('%Y-%m-%d %H:%M:%S')  # Format tanggal dan waktu
        f.write(f'{name},{dtString}\n')
        

# Memuat gambar dan mempelajari wajah dengan folder path absolut
path = r'C:\Users\jokos\Desktop\latihan pyton\training -ai2024\Absen\images'  # Folder dengan gambar referensi
if not os.path.exists(path):
    raise FileNotFoundError(f"Folder '{path}' tidak ditemukan. Pastikan folder ini ada di direktori yang sama dengan skrip Anda.")

images = []
classNames = []
myList = os.listdir(path)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    if curImg is not None:  # Memastikan gambar berhasil dimuat
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])

def find_encodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img)
        if encodings:  # Memastikan ada encoding yang ditemukan
            encodeList.append(encodings[0])
    return encodeList

encodeListKnown = find_encodings(images)

# Membaca wajah dari kamera dan mencocokkan
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            mark_attendance(name)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
