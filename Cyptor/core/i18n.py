import yaml
from pathlib import Path
import os
from typing import Any
from debug import CannotReadLocaleError

DEFAULT_I18N = {'language': 'en-US', 'language_name': 'English', 'language_names': {'zh-CN': '英语'}, 'version': '0.1.0 Alpha', 'common': {'app': {'title': 'Cyptor by Cyan3771 Version {0}'}, 'quit': 'Quit', 'file': {'select': 'Select File:', 'button': {
    'tooltip': 'Click to select file'}}}, 'home': {'welcome': 'Welcome to Cyptor!', 'buttons': {'encrypt': '🔒 Encrypt File', 'decrypt': '🔓 Decrypt File', 'settings': '⚙️ Settings', 'about': 'ℹ️ About'}}, 'encryption': {'title': 'Encrypt File'}, 'errors': {}
}


def mergeDict(default: dict, user_data: dict) -> dict:
    """合并字典"""
    result = default.copy()
    for key, value in user_data.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = mergeDict(result[key], value)
        else:
            result[key] = value
    return result


def loadYaml(file_path: str | Path) -> dict:
    """读取YAML文件"""

    path = Path(file_path)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data
    except Exception as e:
        raise CannotReadLocaleError(e) from e


class LocaleNode:
    """国际化资源节点"""

    def __init__(self, data: dict, parent_path: str = ""):
        self._data = data
        self._parent_path = parent_path

    def __getattr__(self, name: str) -> Any:
        # 如果键存在
        if name in self._data:
            value = self._data[name]
            if isinstance(value, dict):
                # 构建子节点路径
                new_path = f"{self._parent_path}.{name}" if self._parent_path else name
                return LocaleNode(value, new_path)
            return value

        # 键不存在返回占位符
        missing_path = f"{self._parent_path}.{name}" if self._parent_path else name
        return f"{{MISSING: {missing_path}}}"

    def __getitem__(self, key):
        # 支持key访问
        return self.__getattr__(key)

    def get(self, key: str, default=None):
        try:
            return self.__getattr__(key)
        except AttributeError:
            return default

    def __repr__(self):
        return f"LocaleNode({self._data})"


def scanLocales(localesDir: str | Path = "locales") -> dict:
    """
    扫描 locales 文件夹下所有语言文件
    返回结构：
    {
        "zh-CN": {
            "name": "简体中文",
            "version": "0.1.0 Alpha",
            "fileName": "zh-CN.yml",
            "languageNames": {
                "en-US": "Chinese (Simplified)"
            }
        }
    }
    """
    localesPath = Path(localesDir)
    result = {}

    for file in localesPath.glob("*.yml"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}

            langCode = data.get("language", "")
            langName = data.get("language_name", "")
            version = data.get("version", "")
            langNames = data.get("language_names", {})

            if langCode and langName and version and langNames:
                result[langCode] = {
                    "name": langName,
                    "version": version,
                    "fileName": file.name,
                    "languageNames": langNames
                }
        except Exception as e:
            raise CannotReadLocaleError(e) from e

    return result


def loadI18n(langCode: str = "zh-CN") -> LocaleNode:
    """加载国际化资源"""
    locales = scanLocales()
    langFile = locales.get(langCode, {}).get("fileName")
    if not langFile:
        return LocaleNode(DEFAULT_I18N)

    localeData = loadYaml(os.path.join("locales", langFile)) or {}

    return LocaleNode(mergeDict(DEFAULT_I18N, localeData, ))


if __name__ == "__main__":
    # 测试
    loadI18n()
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    print("当前工作目录：", os.getcwd())

    print("测试语言节点功能")
    data = LocaleNode({"A": {"B": "Hello", "C": {"D": "Cyan3771"}}})
    print(data.A.B)
    print(data.A.C.D)
    print(data.A.C.Cyan3771)
    print(data)

    print("\n测试加载YAML文件")
    data = loadYaml("locales/en-US.yml")
    print(data)

    print("\n测试扫描语言文件")
    locales = scanLocales()
    print("扫描结果:", locales)
