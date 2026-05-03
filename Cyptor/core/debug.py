import traceback


def getFullError(exc: Exception) -> str:
    """获取完整的错误信息"""
    return "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))


class CryptoError(Exception):
    """加密或解密错误"""

    def __init__(self, message: str | Exception):
        message = getFullError(message) if isinstance(
            message, Exception) else message
        super().__init__(message)


class AlgorithmNotSupportedError(CryptoError):
    """不支持的算法错误"""

    def __init__(self, algorithm: str):
        self.algorithm = algorithm
        super().__init__(f"Unsupported algorithm: {algorithm}")


class EncryptionError(CryptoError):
    """加密错误"""

    def __init__(self, message: str | Exception):
        message = getFullError(message) if isinstance(
            message, Exception) else message
        super().__init__(message)


class DecryptionError(CryptoError):
    """解密错误"""

    def __init__(self, message: str | Exception):
        message = getFullError(message) if isinstance(
            message, Exception) else message
        super().__init__(message)


class InvalidPasswordError(DecryptionError):
    """无效密码错误"""


class FileError(Exception):
    """文件错误"""

    def __init__(self, message: str | Exception):
        message = getFullError(message) if isinstance(
            message, Exception) else message
        super().__init__(message)


class CannotWriteFileError(FileError):
    """无法写入文件错误"""


class CannotWriteConfigError(CannotWriteFileError):
    """无法写入配置文件错误"""


class CannotInitConfigError(CannotWriteConfigError):
    """无法初始化配置文件错误"""


class CannotReadFileError(FileError):
    """无法读取文件错误"""


class CannotReadConfigError(CannotReadFileError):
    """无法读取配置文件错误"""


class CannotReadLocaleError(CannotReadFileError):
    """无法读取语言文件错误"""
