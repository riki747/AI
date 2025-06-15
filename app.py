from flask import Flask, render_template, Response, redirect, url_for
import emotion_detector

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(emotion_detector.gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start', methods=['POST'])
def start_detection():
    emotion_detector.is_running = True
    return "Deteksi dimulai."

@app.route('/stop')
def stop_detection():
    emotion_detector.is_running = False
    return "Deteksi dihentikan."

if __name__ == '__main__':
    app.run(debug=True)
