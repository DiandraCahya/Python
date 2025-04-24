import cv2
import numpy as np
import mediapipe as mp
import time

# Inisialisasi MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Inisialisasi Keyboard Virtual
keys = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M', 'Del']  # Tombol Del untuk menghapus
]
key_size = 60
margin = 10

# Fungsi untuk menggambar keyboard
def draw_keyboard(frame, keys, pressed_key=None):
    for row_index, row in enumerate(keys):
        for col_index, key in enumerate(row):
            x = margin + col_index * (key_size + margin)
            y = margin + row_index * (key_size + margin) + 100

            # Warna tombol
            if pressed_key == key:
                color = (0, 255, 0)
            else:
                color = (255, 0, 0)

            # Gambar tombol
            cv2.rectangle(frame, (x, y), (x + key_size, y + key_size), color, -1)
            cv2.putText(frame, key, (x + 20, y + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    return frame

# Fungsi untuk mendeteksi jika jari menyentuh tombol
def detect_key_press(landmark, keys):
    x, y = int(landmark.x * frame_width), int(landmark.y * frame_height)

    for row_index, row in enumerate(keys):
        for col_index, key in enumerate(row):
            key_x = margin + col_index * (key_size + margin)
            key_y = margin + row_index * (key_size + margin) + 100
            if key_x <= x <= key_x + key_size and key_y <= y <= key_y + key_size:
                return key
    return None

# Variabel untuk menyimpan teks yang diketik
typed_text = ""
last_pressed_key = None
last_press_time = 0

# Video Capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame horizontal
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape

    # Konversi ke RGB untuk MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    pressed_key = None
    num_fingers = 0

    # Jika ada tangan terdeteksi
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Gambar tangan pada frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Hitung jumlah jari yang terangkat
            landmarks = hand_landmarks.landmark
            finger_tips = [8, 12]  # Index finger tip and middle finger tip
            num_fingers = sum(landmarks[tip].y < landmarks[tip - 2].y for tip in finger_tips)

            # Ambil koordinat ujung telunjuk (jari ke-8)
            index_tip = landmarks[8]

            # Deteksi tombol yang ditekan jika hanya 1 jari terangkat
            if num_fingers == 1:
                pressed_key = detect_key_press(index_tip, keys)

                # Anti-Duplicate Press
                if pressed_key and (pressed_key != last_pressed_key or time.time() - last_press_time > 0.5):
                    if pressed_key == "Del" and typed_text:  # Hapus huruf terakhir
                        typed_text = typed_text[:-1]
                    elif pressed_key != "Del":
                        typed_text += pressed_key
                    last_pressed_key = pressed_key
                    last_press_time = time.time()
            else:
                last_pressed_key = None

    # Gambar keyboard
    frame = draw_keyboard(frame, keys, pressed_key)

    # Tampilkan teks yang sudah diketik
    cv2.putText(frame, f"Typed: {typed_text}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    # Tampilkan frame
    cv2.imshow("Virtual Keyboard", frame)

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Simpan teks ke file
with open("typed_text.txt", "w") as file:
    file.write(typed_text)

# Bersihkan setelah selesai
cap.release()
cv2.destroyAllWindows()
