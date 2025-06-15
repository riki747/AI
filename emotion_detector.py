import cv2
import numpy as np
import threading
import time
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from voice_util import speak_emotion

# Load model dan face detector
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
model = load_model('fer2013_mini_XCEPTION.119-0.65.hdf5', compile=False)

EMOTIONS = ["Marah", "Jijik", "Takut", "Senang", "Sedih", "Terkejut", "Netral"]
is_running = False  # status global deteksi

def speak_async(text):
    threading.Thread(target=speak_emotion, args=(text,), daemon=True).start()

def gen_frames():
    global is_running
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("Tidak dapat membuka webcam.")
        return

    emotion_counters = {emotion: 0 for emotion in EMOTIONS}
    last_spoken_time = time.time()
    speak_delay = 5  # detik
    last_label = None

    while True:
        if not is_running:
            time.sleep(0.1)
            continue

        ret, frame = cap.read()
        if not ret:
            break

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

            # Gambar kotak dan label
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

            for emo in EMOTIONS:
                if emo == label:
                    emotion_counters[emo] += 1
                else:
                    emotion_counters[emo] = 0

            if emotion_counters[label] >= 5 and (time.time() - last_spoken_time) > speak_delay:
                if label != last_label:
                    # Suara dengan penyemangat
                    messages = {
                        "Sedih": "Semangat ya, kamu terlihat sedih.",
                        "Senang": "Wah kamu terlihat senang sekali, bagus itu!",
                        "Marah": "Tenang dulu ya, jangan terlalu emosi.",
                        "Takut": "Gak apa-apa, semua akan baik-baik aja kok.",
                        "Terkejut": "Kaget ya? Ada apa tuh?",
                        "Jijik": "Ups, ada yang gak enak ya?",
                        "Netral": "Kamu terlihat tenang, tetap seperti itu ya."
                    }
                    speak_async(messages.get(label, f"Kamu terlihat {label.lower()}"))
                    last_spoken_time = time.time()
                    last_label = label
                    emotion_counters[label] = 0

        else:
            cv2.putText(frame, "Wajah tidak terdeteksi", (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()
