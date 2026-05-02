import yaml
from pathlib import Path
import os
from typing import Any
from core.config import loadConfig


def loadYaml(file_path: str | Path) -> dict:
    """读取YAML文件"""

    path = Path(file_path)
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data


class LocaleNode(dict):
    """语言节点"""

    def __init__(self, data: dict, parentPath: str = ""):
        super().__init__(data)
        self._parentPath = parentPath

    def __getattr__(self, name) -> Any:
        full = f"{self._parentPath}.{name}" if self._parentPath else name
        if name in self:
            val = self[name]
            if isinstance(val, dict):
                return LocaleNode(val, full)
            return val
        return f"<!{full}>"


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
        except Exception:
            continue

    return result


def loadI18n(langCode: str = "zh-CN") -> LocaleNode:
    """加载国际化资源"""
    locales = scanLocales()
    langFile = locales.get(langCode, {}).get("fileName")

    localeData = loadYaml(os.path.join("locales", langFile)) or {}
    return LocaleNode(localeData)


if __name__ == "__main__":
    # 测试
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    print("当前工作目录：", os.getcwd())

    print("测试语言节点功能")
    data = LocaleNode({"A": {"B": "Hello", "C": {"D": "Cyan3771"}}})
    print(data.A.B)
    print(data.A.C.D)
    print(data.A.C.Cyan3771)
    print(data)

    print("\n测试加载YAML文件")
    data = loadYaml("locales/zh-CN.yml")
    print(data)

    print("\n测试扫描语言文件")
    locales = scanLocales()
    print("扫描结果:", locales)
