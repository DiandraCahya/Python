import cv2
import mediapipe as mp
import numpy as np

# Inisialisasi MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Fungsi untuk menghitung jumlah jari yang terangkat
def count_fingers(hand_landmarks):
    finger_tips = [8, 12, 16, 20]  # Indeks untuk ujung jari (telunjuk, tengah, manis, kelingking)
    finger_base = [5, 9, 13, 17]  # Indeks untuk pangkal jari
    
    fingers = 0
    
    # Cek setiap jari
    for tip, base in zip(finger_tips, finger_base):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[base].y:
            fingers += 1
    
    return fingers

# Inisialisasi canvas untuk menggambar
canvas = None

# Buka kamera
cap = cv2.VideoCapture(0)

prev_x, prev_y = 0, 0
drawing_mode = False
erasing_mode = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Flip gambar horizontal agar seperti cermin
    frame = cv2.flip(frame, 1)
    
    if canvas is None:
        canvas = np.zeros(frame.shape, dtype=np.uint8)
    
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
            
            # Dapatkan koordinat ujung jari telunjuk
            index_finger_tip = hand_landmarks.landmark[8]
            x = int(index_finger_tip.x * frame.shape[1])
            y = int(index_finger_tip.y * frame.shape[0])
            
            # Mode menggambar jika dua jari terangkat
            if finger_count == 2:
                drawing_mode = True
                erasing_mode = False
                if prev_x != 0 and prev_y != 0:
                    cv2.line(canvas, (prev_x, prev_y), (x, y), (0, 0, 255), 10)  # Warna merah (BGR)
                prev_x, prev_y = x, y
            
            # Mode menghapus jika empat jari terangkat
            elif finger_count == 4:
                drawing_mode = False
                erasing_mode = True
                cv2.circle(canvas, (x, y), 20, (0, 0, 0), -1)
            
            else:
                drawing_mode = False
                erasing_mode = False
                prev_x, prev_y = 0, 0
            
            # Tampilkan jumlah jari dan mode
            mode_text = "Menggambar" if drawing_mode else ("Menghapus" if erasing_mode else "Idle")
            cv2.putText(frame, f'Jari: {finger_count} - Mode: {mode_text}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Gabungkan frame dengan canvas (opacity penuh)
    output = cv2.addWeighted(frame, 1, canvas, 1, 0)
    
    # Tampilkan frame
    cv2.imshow('Gambar Gambar Muehehehehhe', output)
    
    # Keluar jika tombol 'q' ditekan
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Tutup kamera dan jendela
cap.release()
cv2.destroyAllWindows()
