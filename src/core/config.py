import json
from pathlib import Path
from core.debug import CyptorError, ErrorCode

VERSION = "0.1.0"
PRE_RELEASE = True
DEFAULT_CONFIG = {
    "version": VERSION,
    "language": "zh-CN"
}


def initJson(path: str | Path):
    """初始化JSON文件"""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f)
    except Exception as e:
        raise CyptorError(code=ErrorCode.CONFIG_INIT_FAILED, params={"path": str(
            path)}, message=f"Failed to initialize config file: {path}", debug={"exception": str(e)}) from e


def loadJson(file_path: str | Path) -> dict:
    """读取JSON文件"""

    path = Path(file_path)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        initJson(path)
        return DEFAULT_CONFIG
    except Exception as e:
        initJson(path)
        raise CyptorError(code=ErrorCode.CONFIG_READ_FAILED, params={"path": str(
            path)}, message=f"Failed to read config file: {path}", debug={"exception": str(e)}) from e


def loadConfig() -> dict:
    """加载配置文件"""
    config = loadJson("config.json")
    for key, value in DEFAULT_CONFIG.items():
        if key not in config:
            config[key] = value
    return config


if __name__ == "__main__":
    pass
