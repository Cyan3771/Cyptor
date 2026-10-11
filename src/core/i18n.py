import yaml
from pathlib import Path
import os
from typing import Any
import main

from core.debug import CyptorError, ErrorCode

DEFAULT_I18N = {'language': 'en-US', 'language_name': 'English', 'language_name_in_other_languages': {'zh-CN': '英语'}, 'version': '0.1.0', 'common': {'app': {'title': 'Cyptor by Cyan3771 Version {0}'}, 'quit': 'Quit', 'file': {'select': 'Select File:', 'button': {
    'tooltip': 'Click to select file'}}}, 'home': {'welcome': 'Welcome to Cyptor!', 'buttons': {'encrypt': '🔒 Encrypt File', 'decrypt': '🔓 Decrypt File', 'settings': '⚙️ Settings', 'about': 'ℹ️ About'}}, 'encryption': {'title': 'Encrypt File'}, 'errors': {}
}
LOCALES_DIR = main.PROJECT_ROOT / "locales"


def mergeDict(default: dict, user_data: dict) -> dict:
    """合并字典"""
    result = default.copy()
    for key, value in user_data.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = mergeDict(result[key], value)
        else:
            result[key] = value
    return result


def loadYaml(path: Path) -> dict:
    """读取YAML文件"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data
    except Exception as e:
        raise CyptorError(code=ErrorCode.LOCALE_READ_FAILED, params={"path": str(
            path)}, message=f"Failed to read locale file: {path}", debug={"exception": str(e)}) from e


class _Missing:
    """缺失键的占位对象"""

    __slots__ = ("path",)

    def __init__(self, path: str) -> None:
        self.path = path

    def __str__(self) -> str:
        return f"{{MISSING: {self.path}}}"

    def __repr__(self) -> str:
        return f"_Missing({self.path!r})"

    def __bool__(self) -> bool:
        return False

    def __eq__(self, other: object) -> bool:
        if isinstance(other, _Missing):
            return self.path == other.path
        return NotImplemented

    def __hash__(self) -> int:
        return hash(("_Missing", self.path))

    def __format__(self, spec: str) -> str:
        return format(str(self), spec)

    def __getattr__(self, name: str) -> "_Missing":
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)
        new_path = f"{self.path}.{name}" if self.path else name
        return _Missing(new_path)

    def __getitem__(self, key: str) -> "_Missing":
        new_path = f"{self.path}.{key}" if self.path else key
        return _Missing(new_path)


def is_missing(value: Any) -> bool:
    """判断一个值是不是缺失标记"""
    return isinstance(value, _Missing)


class LocaleNode:
    """国际化资源节点"""

    def __init__(self, data: dict, parent_path: str = "") -> None:
        object.__setattr__(self, "_data", data)
        object.__setattr__(self, "_parent_path", parent_path)

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise AttributeError(name)

        data = object.__getattribute__(self, "_data")
        parent_path = object.__getattribute__(self, "_parent_path")

        if name in data:
            value = data[name]
            if isinstance(value, dict):
                new_path = f"{parent_path}.{name}" if parent_path else name
                return LocaleNode(value, new_path)
            return value

        missing_path = f"{parent_path}.{name}" if parent_path else name
        return _Missing(missing_path)

    def __getitem__(self, key: str) -> Any:
        return self.__getattr__(key)

    def __contains__(self, key: str) -> bool:
        return key in object.__getattribute__(self, "_data")

    def get(self, key: str, default: Any = None) -> Any:
        value = self.__getattr__(key)
        if is_missing(value):
            return default
        return value

    def __repr__(self) -> str:
        data = object.__getattribute__(self, "_data")
        parent_path = object.__getattribute__(self, "_parent_path")
        if parent_path:
            return f"LocaleNode({data!r}, path={parent_path!r})"
        return f"LocaleNode({data!r})"


def scanLocales(localesDir: Path = LOCALES_DIR) -> dict:
    """
    扫描 locales 文件夹下所有语言文件
    返回结构：
    {
        "zh-CN": {
            "name": "简体中文",
            "version": "0.1.0",
            "fileName": "zh-CN.yml",
            "languageNames": {
                "en-US": "Chinese (Simplified)"
            }
        }
    }
    """
    result = {}

    for file in localesDir.glob("*.yml"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}

            langCode = data.get("language", "")
            langName = data.get("language_name", "")
            version = data.get("version", "UNKNOWN")
            langNames = data.get("language_name_in_other_languages", {})

            if langCode and langName:
                result[langCode] = {
                    "name": langName,
                    "version": version,
                    "fileName": file.name,
                    "languageNames": langNames
                }
        except Exception as e:
            raise CyptorError(code=ErrorCode.LOCALE_READ_FAILED, params={"path": str(
                file)}, message=f"Failed to read locale file: {file}", debug={"exception": str(e)}) from e

    return result


def loadI18n(langCode: str = "zh-CN") -> LocaleNode:
    """加载国际化资源"""
    locales = scanLocales()
    langFile = locales.get(langCode, {}).get("fileName")
    if not langFile:
        return LocaleNode(DEFAULT_I18N)

    localeData = loadYaml(LOCALES_DIR / langFile) or {}

    return LocaleNode(mergeDict(DEFAULT_I18N, localeData, ))


if __name__ == "__main__":
    data = LocaleNode({"A": {"B": "Hello", "C": {"D": "Cyan3771"}}})

    print("=== 1. 基本访问 ===")
    print("data.A.B        =", repr(data.A.B))
    print("data.A.C.D      =", repr(data.A.C.D))
    print('data["A"]["B"]  =', repr(data["A"]["B"]))

    print("\n=== 2. 缺键 ===")
    print("data.X          =", repr(data.X))
    print("str(data.X)     =", str(data.X))
    print("data.X.Y.Z      =", repr(data.X.Y.Z))
    print("str(data.X.Y.Z) =", str(data.X.Y.Z))
    print("data.A.X        =", repr(data.A.X))
    print("str(data.A.X)   =", str(data.A.X))
    print("bool(data.X)    =", bool(data.X))
    print("is_missing(data.X) =", is_missing(data.X))

    print("\n=== 3. get 回退 ===")
    print('data.get("X")           =', repr(data.get("X")))
    print('data.get("X", "fb")     =', repr(data.get("X", "fb")))
    print('data.get("A")           =', repr(data.get("A")))
    print('is_missing(data.get("A")) =', is_missing(data.get("A")))

    print("\n=== 4. in ===")
    print('"A" in data  =', "A" in data)
    print('"X" in data  =', "X" in data)

    print("\n=== 5. 相等性 ===")
    print("data.X == data.X =", data.X == data.X)
    print("data.X == data.Y =", data.X == data.Y)
    print('data.X == "abc"  =', data.X == "abc")

    print("\n=== 6. f-string ===")
    print("f'{data.X}' =", f"{data.X}")

    print("\n=== 7. 私有属性 ===")
    try:
        data._foo
        print("data._foo 没抛异常（不对）")
    except AttributeError as e:
        print("data._foo 抛了 AttributeError:", e)

    print("\n=== 8. repr ===")
    print("repr(data)   =", repr(data))
    print("repr(data.A) =", repr(data.A))
    print("repr(data.X) =", repr(data.X))

    print("\n=== 9. mergeDict ===")
    merged = mergeDict({"a": 1, "b": {"c": 2}}, {"b": {"d": 3}, "e": 4})
    print("merged =", merged)

    print("\n=== 10. DEFAULT_I18N ===")
    locale = LocaleNode(DEFAULT_I18N)
    print("locale.language                    =", repr(locale.language))
    print("locale.version                     =", repr(locale.version))
    print("locale.home.welcome                =", repr(locale.home.welcome))
    print("locale.home.buttons.encrypt        =",
          repr(locale.home.buttons.encrypt))
    print("locale.common.app.title            =", repr(locale.common.app.title))
    print("locale.errors                      =", repr(locale.errors))

    print("\n=== 11. scanLocales ===")
    print("LOCALES_DIR =", LOCALES_DIR)
    print("目录存在?   =", LOCALES_DIR.exists())
    print("目录内容    =", list(LOCALES_DIR.glob("*"))
          if LOCALES_DIR.exists() else "目录不存在")
    locales = scanLocales()
    print("扫描结果    =", locales)
    print("语言码列表  =", list(locales.keys()))

    print("\n=== 12. loadI18n 兜底 ===")
    i18n = loadI18n("not-exist")
    print("i18n.home.welcome =", repr(i18n.home.welcome))

    print("\n=== 13. 缺键路径在真实 i18n 里 ===")
    print("i18n.home.typo         =", repr(i18n.home.typo))
    print("str(i18n.home.typo)    =", str(i18n.home.typo))
    print("i18n.errors.SOME_CODE  =", repr(i18n.errors.SOME_CODE))
    print("str(i18n.errors.SOME_CODE) =", str(i18n.errors.SOME_CODE))
