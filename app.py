from flask import Flask, render_template, request
import threading
import emotion_detector

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def start_detection():
    try:
        emotion_detector.run()  # Langsung jalankan tanpa threading
        return "Deteksi dimulai."
    except Exception as e:
        return f"Terjadi error: {e}", 500

        
@app.route('/stop', methods=['POST'])
def stop_detection():
    try:
        # Hentikan deteksi wajah
        emotion_detector.stop_detection()
        return "Deteksi dihentikan."
    except Exception as e:
        return f"Terjadi error: {e}", 500
    
