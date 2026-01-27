import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from voice_grammar import build_grammar
from UI.floating_panel import update_status

MODEL_PATH = "models/vosk/vosk-model-en-us-0.22-lgraph"
SAMPLE_RATE = 16000
CONFIDENCE_THRESHOLD = 0.5


class VoiceListener:
    def __init__(self):
        self.model = Model(MODEL_PATH)

        grammar = json.dumps(build_grammar())
        self.recognizer = KaldiRecognizer(self.model, SAMPLE_RATE, grammar)
        self.recognizer.SetWords(True)

        self.audio_queue = queue.Queue()
        self.active = False

    def _callback(self, indata, frames, time, status):
        if self.active:
            self.audio_queue.put(bytes(indata))

    def listen_continuous(self):
        self.active = True
        update_status("🎤 Listening...")
        with sd.RawInputStream(
            samplerate=SAMPLE_RATE,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=self._callback
        ):
            while self.active:
                data = self.audio_queue.get()
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text", "").lower()

                    if not text:
                        continue

                    confidence = self._confidence(result)
                    if confidence < CONFIDENCE_THRESHOLD:
                        continue

                    update_status(f"Recognized: {text}")
                    return text

    def _confidence(self, result):
        words = result.get("result", [])
        if not words:
            return 0.0
        return sum(w["conf"] for w in words) / len(words)

    def stop(self):
        self.active = False
