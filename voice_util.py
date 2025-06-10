from gtts import gTTS
import pygame
import time
import os

def speak_emotion(text):
    try:
        # Generate voice
        tts = gTTS(text=text, lang='id')
        tts.save("temp_voice.mp3")

        # Init mixer
        pygame.mixer.init()
        pygame.mixer.music.load("temp_voice.mp3")
        pygame.mixer.music.play()

        # Tunggu hingga selesai
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.music.unload()
        pygame.mixer.quit()
        os.remove("temp_voice.mp3")

    except Exception as e:
        print("Gagal menghasilkan suara:", e)
