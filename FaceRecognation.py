from deepface import DeepFace
import cv2

def capture_image():
    cap = cv2.VideoCapture(0)
    print("\n--- Kamera Aktif ---")
    print("Tekan 's' untuk menangkap gambar atau 'q' untuk keluar.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Gagal mengakses kamera.")
            break

        cv2.imshow("Kamera", frame)

        key = cv2.waitKey(1)
        if key & 0xFF == ord('s'):
            cv2.imwrite("captured_image.jpg", frame)
            print("\n✅ Gambar berhasil diambil dan disimpan sebagai 'captured_image.jpg'")
            break
        elif key & 0xFF == ord('q'):
            print("\n❌ Keluar tanpa menangkap gambar.")
            break

    cap.release()
    cv2.destroyAllWindows()

def recognize_face(reference_images, captured_image_path):
    print("\n--- Proses Pengenalan Wajah ---")
    try:
        for name, image_path in reference_images.items():
            result = DeepFace.verify(img1_path=image_path, img2_path=captured_image_path)
            if result["verified"]:
                print(f"✅ Ini adalah {name}.")
                return
        print("❌ Orang tidak dikenal: Wajah tidak cocok dengan siapa pun di daftar referensi.")
    except Exception as e:
        print("⚠️ Terjadi kesalahan:", e)

if __name__ == "__main__":
    print("Langkah 1: Pastikan Anda memiliki gambar referensi untuk setiap teman.")

    reference_images = {
        "Yavi": "Yavi.jpg",      
        "Theo": "Theo.jpg",      
        "Diandra": "Diandra.jpg", 
        "Kak Ruby": "Kak Ruby.jpg"
    }

    capture_image()

    captured_image = "captured_image.jpg"
    recognize_face(reference_images, captured_image)
