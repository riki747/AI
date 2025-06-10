import cv2
import numpy as np
import threading
import time
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from voice_util import speak_emotion

def run():
    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    model = load_model('D:\SEMESTER 4\AI\FD-Flask/fer2013_mini_XCEPTION.119-0.65.hdf5', compile=False)
    EMOTIONS = ["Marah", "Jijik", "Takut", "Senang", "Sedih", "Terkejut", "Netral"]

    def speak_async(text):
        threading.Thread(target=speak_emotion, args=(text,), daemon=True).start()

    emotion_counters = {emotion: 0 for emotion in EMOTIONS}
    last_spoken_time = time.time()
    speak_delay = 5

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Tidak dapat membuka webcam.")
        return

    while True:
        try:
            ret, frame = cap.read()
            if not ret:
                print("Gagal membaca frame dari kamera.")
                continue

            frame = cv2.resize(frame, (640, 480))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            if len(faces) > 0:
                x, y, w, h = faces[0]
                roi_gray = gray[y:y+h, x:x+w]
                roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

                roi = roi_gray.astype("float32") / 255.0
                roi = np.expand_dims(roi, axis=-1)
                roi = np.expand_dims(roi, axis=0)

                preds = model.predict(roi, verbose=0)[0]
                label = EMOTIONS[np.argmax(preds)]

                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.putText(frame, label, (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

                for emo in EMOTIONS:
                    if emo == label:
                        emotion_counters[emo] += 1
                    else:
                        emotion_counters[emo] = 0

                if emotion_counters[label] >= 5 and (time.time() - last_spoken_time) > speak_delay:
                    if label == "Sedih":
                        speak_async("Semangat ya, kamu terlihat sedih.")
                    elif label == "Senang":
                        speak_async("Wah kamu terlihat senang sekali, bagus itu!")
                    elif label == "Marah":
                        speak_async("Tenang dulu ya, jangan terlalu emosi.")
                    elif label == "Takut":
                        speak_async("Gak apa-apa, semua akan baik-baik aja kok.")
                    elif label == "Terkejut":
                        speak_async("Kaget ya? Ada apa tuh?")
                    elif label == "Jijik":
                        speak_async("Ups, ada yang gak enak ya?")
                    elif label == "Netral":
                        speak_async("Kamu terlihat tenang, tetap seperti itu ya.")

                    last_spoken_time = time.time()
                    emotion_counters[label] = 0

            else:
                cv2.putText(frame, "Wajah tidak terdeteksi", (30, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

            cv2.imshow('Real-time Emotion Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except Exception as e:
            print("Error:", e)
            continue

    cap.release()
    cv2.destroyAllWindows()
