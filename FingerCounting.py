import cv2
import mediapipe as mp

# Inisialisasi MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

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

# Buka kamera
cap = cv2.VideoCapture(0)

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
            
            # Tampilkan jumlah jari
            cv2.putText(frame, f'Jari: {finger_count}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Tampilkan frame
    cv2.imshow('Deteksi Jari', frame)
    
    # Keluar jika tombol 'q' ditekan
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Tutup kamera dan jendela
cap.release()
cv2.destroyAllWindows()