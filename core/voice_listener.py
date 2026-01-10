import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import os

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "models",
    "vosk",
    "vosk-model-en-us-0.22-lgraph"
)

SAMPLE_RATE = 16000


class VoiceListener:
    def __init__(self):
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"VOSK model not found at {MODEL_PATH}")

        print("🔊 Loading VOSK model...")
        self.model = Model(MODEL_PATH)

        # Grammar-based recognizer (IMPORTANT for lgraph)
        grammar = [
            "open chrome",
            "open notepad",
            "close chrome",
            "start camera",
            "stop camera",
            "scroll up",
            "scroll down",
            "click",
            "double click",
            "exit voice",
            "shutdown system"
        ]

        self.recognizer = KaldiRecognizer(
            self.model,
            SAMPLE_RATE,
            json.dumps(grammar)
        )

        self.q = queue.Queue()
        self.running = False

    def _audio_callback(self, indata, frames, time, status):
        if status:
            print("⚠️ Audio status:", status)
        self.q.put(bytes(indata))

    def listen(self):
        self.running = True
        print("🎤 Voice mode ACTIVE (listening...)")

        with sd.RawInputStream(
            samplerate=SAMPLE_RATE,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=self._audio_callback,
        ):
            while self.running:
                data = self.q.get()

                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text", "").strip()

                    if text:
                        if text == "exit voice":
                            self.stop()
                        return text

    def stop(self):
        self.running = False
        print("🎤 Voice mode STOPPED")
