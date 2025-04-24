import cv2
import mediapipe as mp
import math
import numpy as np

# Inisialisasi MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Faktor kalibrasi (disesuaikan berdasarkan penggaris dan kamera)
cm_per_pixel = 0.026  # Contoh nilai, sesuaikan dengan hasil kalibrasi

# Fungsi untuk menghitung jarak antara dua titik
def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance

# Fungsi untuk smoothing nilai jarak
def smooth_distance(distance, history, smoothing_window=5):
    history.append(distance)
    if len(history) > smoothing_window:
        history.pop(0)
    return np.mean(history)

# Inisialisasi history untuk smoothing
distance_history = []

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
    
    landmarks_positions = []  # Menyimpan posisi landmark jari telunjuk (titik 8)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Gambar landmark tangan
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Ambil posisi landmark telunjuk (titik 8)
            index_finger_tip = hand_landmarks.landmark[8]
            h, w, _ = frame.shape
            landmarks_positions.append((int(index_finger_tip.x * w), int(index_finger_tip.y * h)))

    # Hitung jarak jika ada dua tangan terdeteksi
    if len(landmarks_positions) == 2:
        point1, point2 = landmarks_positions
        distance_in_pixels = calculate_distance(point1, point2)
        distance_in_cm = distance_in_pixels * cm_per_pixel

        # Terapkan smoothing
        smoothed_distance = smooth_distance(distance_in_cm, distance_history)
        
        # Gambar garis antara dua titik telunjuk
        cv2.line(frame, point1, point2, (0, 255, 0), 2)
        
        # Tampilkan jarak di tengah garis
        midpoint = ((point1[0] + point2[0]) // 2, (point1[1] + point2[1]) // 2)
        cv2.putText(frame, f'{smoothed_distance:.2f} cm', midpoint, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Tampilkan frame
    cv2.imshow('Jarak Telunjuk', frame)
    
    # Keluar jika tombol 'q' ditekan
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Tutup kamera dan jendela
cap.release()
cv2.destroyAllWindows()
