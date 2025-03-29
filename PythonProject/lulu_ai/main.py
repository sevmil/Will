from core.voice_interface import VoiceInterface
from core.nlp_engine import ConversationEngine
from core.device_manager import SmartHomeManager
from core.memory_store import MemoryStorage
import time


class LuluAI:
    def __init__(self):
        self.voice = VoiceInterface()
        self.nlp = ConversationEngine()
        self.devices = SmartHomeManager()
        self.memory = MemoryStorage()

    def run(self):
        print("=== 陆陆AI助手启动 ===")
        try:
            while True:
                # 语音输入
                input("\n按回车开始对话...")
                user_input = self.voice.listen()
                if not user_input:
                    continue
                print(f"[用户输入] {user_input}")

                # 处理指令
                device_response = self.devices.execute_command(user_input)
                if device_response:
                    response = device_response
                else:
                    response = self.nlp.generate(user_input)

                # 输出与存储
                print(f"[系统响应] {response}")
                self.voice.speak(response)
                self.memory.save(user_input, response)

                time.sleep(0.5)  # 防止过热

        except KeyboardInterrupt:
            print("\n=== 系统安全关闭 ===")


if __name__ == "__main__":
    ai = LuluAI()
    ai.run()