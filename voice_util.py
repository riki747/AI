from gtts import gTTS
import pygame
import time
import os

def speak_emotion(text):
    try:
        tts = gTTS(text=text, lang='id')
        filename = "temp_voice.mp3"
        tts.save(filename)

        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.music.stop()
        pygame.mixer.quit()

        time.sleep(0.2)
        if os.path.exists(filename):
            os.remove(filename)

    except Exception as e:
        print("Gagal menghasilkan suara:", e)

