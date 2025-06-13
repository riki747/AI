from flask import Flask, render_template, Response, request
import threading
import emotion_detector

app = Flask(__name__)

detection_thread = None
detection_running = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_detection():
    global detection_running, detection_thread
    if not detection_running:
        detection_running = True
        emotion_detector.detection_running = True
        detection_thread = threading.Thread(target=emotion_detector.run_detection)
        detection_thread.start()
        return "Deteksi dimulai."
    else:
        return "Deteksi sudah berjalan."

@app.route('/stop', methods=['POST'])
def stop_detection():
    global detection_running
    detection_running = False
    emotion_detector.detection_running = False
    return "Deteksi dihentikan."

@app.route('/video_feed')
def video_feed():
    return Response(emotion_detector.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
