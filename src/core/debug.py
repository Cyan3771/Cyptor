
import traceback
# 错误码定义


class ErrorCode:

    # 加密
    ALGORITHM_NOT_SUPPORTED = "CRYPTO.ALGORITHM_NOT_SUPPORTED"
    ENCRYPT_FAILED = "CRYPTO.ENCRYPT.FAILED"

    # 解密
    DECRYPT_FAILED = "CRYPTO.DECRYPT.FAILED"

    # IO
    FILE_READ_FAILED = "IO.FILE.READ_FAILED"
    FILE_WRITE_FAILED = "IO.FILE.WRITE_FAILED"
    CONFIG_READ_FAILED = "IO.CONFIG.READ_FAILED"
    CONFIG_WRITE_FAILED = "IO.CONFIG.WRITE_FAILED"
    CONFIG_INIT_FAILED = "IO.CONFIG.INIT_FAILED"
    LOCALE_READ_FAILED = "IO.LOCALE.READ_FAILED"

    # 兜底
    UNKNOWN = "UNKNOWN"

    # 错误码参数表
    ERROR_PARAMS: dict[str, tuple[str, ...] | None] = {
        ALGORITHM_NOT_SUPPORTED: ("algorithm",),
        ENCRYPT_FAILED: None,
        DECRYPT_FAILED: None,
        FILE_READ_FAILED: ("path",),
        FILE_WRITE_FAILED: ("path",),
        CONFIG_READ_FAILED: ("path",),
        CONFIG_WRITE_FAILED: ("path",),
        CONFIG_INIT_FAILED: ("path",),
        LOCALE_READ_FAILED: ("path",),
        UNKNOWN: None
    }


# Cyptor 错误定义
class CyptorError(Exception):
    """Cyptor 错误"""

    def __init__(self, code: str = ErrorCode.UNKNOWN, params: dict = {}, message: str = "", debug: dict = {}) -> None:
        super().__init__()
        self.code = code
        self.params = params
        self.message = message
        self.debug = debug

    # 检查参数是否正确
    def check_params(self) -> bool:
        expected_params = ErrorCode.ERROR_PARAMS.get(self.code)
        if expected_params is None:
            return True
        for param in expected_params:
            if param not in self.params:
                return False
        return True

    # 转为字典
    def to_dict(self,) -> dict:
        result = {
            "code": self.code,
            "params": self.params if self.check_params() else None,
            "message": self.message,
            "debug": self.debug
        }
        return result
