import cv2
import mediapipe as mp
import webbrowser
import time
import psutil

# Inisialisasi MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Variabel untuk melacak waktu pembukaan situs
last_opened_time = {1: 0, 2: 0, 3: 0}
delay = 10  # 10 detik

# Variabel untuk melacak waktu deteksi jari
waktu_deteksi_jari_4 = 0
deteksi_jari_4 = False
deteksi_jari_4_durasi = 2  # 2 detik

# Fungsi untuk membuka situs berdasarkan jumlah jari
def buka_situs(jari):
    current_time = time.time()
    if current_time - last_opened_time.get(jari, 0) > delay:
        if jari == 1:
            webbrowser.open('https://www.google.com')
            print("Membuka Google")
        elif jari == 2:
            webbrowser.open('https://www.youtube.com')
            print("Membuka YouTube")
        elif jari == 3:
            webbrowser.open('https://www.facebook.com')
            print("Membuka Facebook")
        last_opened_time[jari] = current_time

# Fungsi untuk menutup semua jendela Microsoft Edge
def tutup_edge():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'msedge.exe':  # Nama proses Microsoft Edge
            try:
                proc.terminate()  # Menutup proses
                proc.wait(timeout=3)  # Menunggu proses benar-benar tertutup
                print("Menutup Microsoft Edge")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

# Fungsi untuk menghitung jumlah jari yang terangkat
def hitung_jari(hand_landmarks):
    jari_terangkat = 0
    jari_tips = [8, 12, 16, 20]
    for tip in jari_tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            jari_terangkat += 1
    return jari_terangkat

# Inisialisasi kamera
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Tidak dapat mengakses kamera")
        break

    # Konversi gambar ke format RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    current_time = time.time()

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            jari = hitung_jari(hand_landmarks)
            
            if jari == 1:
                teks = "Membuka google.com"
            elif jari == 2:
                teks = "Membuka youtube.com"
            elif jari == 3:
                teks = "Membuka facebook.com"
            elif jari == 4:
                teks = "Menunggu 2 detik untuk menutup browser"
                if not deteksi_jari_4:
                    # Jika deteksi jari 4 baru dimulai
                    waktu_deteksi_jari_4 = current_time
                    deteksi_jari_4 = True
                elif current_time - waktu_deteksi_jari_4 >= deteksi_jari_4_durasi:
                    # Jika sudah 2 detik, tutup browser
                    tutup_edge()
                    deteksi_jari_4 = False
            else:
                teks = ""
                # Reset deteksi jika jari bukan 4
                deteksi_jari_4 = False
            
            # Tampilkan teks pada frame
            cv2.putText(frame, teks, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

            # Buka situs jika jumlah jari bukan 4
            if jari != 4:
                buka_situs(jari)

    cv2.imshow('Hand Tracking', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()


