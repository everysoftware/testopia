import json
import subprocess

import speech_recognition as sr
from vosk import Model

recognizer = sr.Recognizer()
recognizer.vosk_model = Model("./models/vosk-rus-small")


def ogg_to_wav(ogg_path: str, wav_path: str | None = None) -> str:
    if wav_path is None:
        wav_path = ogg_path.replace(".ogg", ".wav")
    subprocess.run(["ffmpeg", "-i", ogg_path, wav_path], check=True)
    return wav_path


def stt(wav_path: str) -> str:
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
        text_json = recognizer.recognize_vosk(audio_data, language="russian")
        text = json.loads(text_json)["text"]
        return text
