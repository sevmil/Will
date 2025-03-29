from dataclasses import dataclass
from typing import Dict, Any, Optional
import yaml


@dataclass
class DeviceStatus:
    light: bool = False
    ac_temp: int = 26
    curtain_open: bool = False


class SmartHomeManager:
    def __init__(self, config_path: str = "configs/devices.yaml"):
        self.status = DeviceStatus()
        self._load_config(config_path)

    def _load_config(self, path: str):
        """加载设备配置"""
        with open(path) as f:
            self.config = yaml.safe_load(f)

    def execute_command(self, command: str) -> Optional[str]:
        """执行设备控制指令"""
        cmd = command.lower()
        # 灯光控制
        if any(kw in cmd for kw in ["开灯", "打开灯"]):
            self.status.light = True
            return "灯光已开启"
        elif any(kw in cmd for kw in ["关灯", "关闭灯"]):
            self.status.light = False
            return "灯光已关闭"
        # 温度控制
        elif "调高温度" in cmd:
            self.status.ac_temp += 1
            return f"空调温度已设为{self.status.ac_temp}℃"
        elif "降低温度" in cmd:
            self.status.ac_temp -= 1
            return f"空调温度已设为{self.status.ac_temp}℃"
        return None