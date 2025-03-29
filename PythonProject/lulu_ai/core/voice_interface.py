import speech_recognition as sr
import pyttsx3
from typing import Optional


class VoiceInterface:
    def __init__(self, config_path: str = "configs/voice.yaml"):
        self._load_config(config_path)
        self._init_asr()
        self._init_tts()

    def _load_config(self, path):
        """加载语音配置"""
        # 这里可以添加YAML解析逻辑
        self.sample_rate = 16000
        self.voice_index = 1  # 中文语音索引

    def _init_asr(self):
        """初始化语音识别"""
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)

    def _init_tts(self):
        """初始化语音合成"""
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        if len(voices) > self.voice_index:
            self.engine.setProperty('voice', voices[self.voice_index].id)
        self.engine.setProperty('rate', 160)

    def listen(self) -> Optional[str]:
        """语音转文字"""
        try:
            with self.mic as source:
                print("\n[请说话...]")
                audio = self.recognizer.listen(source, timeout=5)
                return self.recognizer.recognize_google(audio, language='zh-CN')
        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            print(f"ASR错误: {str(e)}")
            return None

    def speak(self, text: str):
        """文字转语音"""
        self.engine.say(text)
        self.engine.runAndWait()