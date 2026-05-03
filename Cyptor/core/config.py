import json
from pathlib import Path
from core.debug import CannotWriteConfigError, CannotReadConfigError, CannotInitConfigError

VERSION = "0.1.0 Alpha"
DEFAULT_CONFIG = {
    "language": "zh-CN"
}


def initJson(path: str | Path):
    """初始化JSON文件"""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump({}, f)
    except Exception as e:
        raise CannotInitConfigError(e) from e


def loadJson(file_path: str | Path) -> dict:
    """读取JSON文件"""

    path = Path(file_path)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        try:
            initJson(path)
            return {}
        except Exception as e:
            raise CannotInitConfigError(e) from e
    except Exception as e:
        initJson(path)
        raise CannotReadConfigError(e) from e


def loadConfig() -> dict:
    """加载配置文件"""
    config = loadJson("config.json")
    for key, value in DEFAULT_CONFIG.items():
        if key not in config:
            config[key] = value
    return config


if __name__ == "__main__":
    pass
