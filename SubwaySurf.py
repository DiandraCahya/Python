import cv2
import mediapipe as mp
from pynput.keyboard import Controller
import time

# Inisialisasi MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Inisialisasi keyboard controller
keyboard = Controller()

# Fungsi untuk menghitung jumlah jari yang terangkat
def count_fingers(hand_landmarks):
    finger_tips = [8, 12, 16, 20]  # Indeks untuk ujung jari (telunjuk, tengah, manis, kelingking)
    thumb_tip = 4  # Indeks untuk ujung ibu jari
    
    fingers = 0
    
    # Cek ibu jari
    if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_tip - 1].x:
        fingers += 1
    
    # Cek jari lainnya
    for tip in finger_tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers += 1
    
    return fingers

# Fungsi untuk menekan tombol sesuai jumlah jari
def press_key(finger_count):
    key_mapping = {0: 's', 1: 'a', 2: 'd', 5: 'w'}
    if finger_count in key_mapping:
        keyboard.press(key_mapping[finger_count])
        keyboard.release(key_mapping[finger_count])

# Buka kamera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Variabel untuk menyimpan jumlah jari terakhir dan waktu perubahan
last_finger_count = -1  # Nilai awal yang tidak valid
time_changed = time.time()  # Waktu awal perubahan jari

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Flip gambar horizontal agar seperti cermin
    frame = cv2.flip(frame, 1)
    
    # Konversi gambar ke RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Proses gambar dengan MediaPipe Hands
    results = hands.process(rgb_frame)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Gambar landmark tangan
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Hitung jumlah jari
            finger_count = count_fingers(hand_landmarks)
            
            # Jika jumlah jari berubah, catat waktu perubahan
            if finger_count != last_finger_count:
                time_changed = time.time()
                last_finger_count = finger_count
            
            # Jika sudah 0,2 detik sejak perubahan terakhir, tekan tombol
            if time.time() - time_changed >= 0.08:
                press_key(finger_count)
                time_changed = float('inf')  # Mencegah pengulangan hingga ada perubahan lagi
            
            # Tampilkan jumlah jari
            cv2.putText(frame, f'Jari: {finger_count}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
        # Reset jumlah jari terakhir jika tidak ada tangan terdeteksi
        last_finger_count = -1
        time_changed = time.time()  # Reset waktu jika tidak ada tangan

    # Tampilkan frame
    cv2.imshow('Deteksi Jari', frame)
    
    # Keluar jika tombol 'q' ditekan
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Tutup kamera dan jendela
cap.release()
cv2.destroyAllWindows()
