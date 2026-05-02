import json
from pathlib import Path

VERSION = "0.1.0 Alpha"
DEFAULT_CONFIG = {
    "language": "zh-CN"
}


def loadJson(file_path: str | Path) -> dict:
    """读取JSON文件"""

    path = Path(file_path)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump({}, f)
            return {}
        except Exception as e:
            raise e
    except Exception as e:
        raise e


def loadConfig() -> dict:
    """加载配置文件"""
    config = loadJson("config.json")
    for key, value in DEFAULT_CONFIG.items():
        if key not in config:
            config[key] = value
    return config


if __name__ == "__main__":
    pass
