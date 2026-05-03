from core.crypto.aes import AES
from core.crypto.chacha20 import ChaCha20
from core.debug import AlgorithmNotSupportedError, EncryptionError, DecryptionError, InvalidPasswordError


class CryptoManager:
    """加密管理器
    初始化：algorithm: str 加密算法
    """
    _ALGORITHM_REGISTRY = {
        "AES-256-CBC": AES,
        "ChaCha20": ChaCha20,
    }

    def __init__(self, algorithm: str):
        # 校验算法是否存在
        if algorithm not in self._ALGORITHM_REGISTRY:
            raise AlgorithmNotSupportedError(algorithm)

        # 创建对应算法实例
        self._crypto = self._ALGORITHM_REGISTRY[algorithm]()

    def encrypt(self, data: bytes, password: str) -> bytes:
        """
        加密
        输入: data: bytes, password: str
        输出: data: bytes
        """
        try:
            return self._crypto.encrypt(data, password)
        except Exception as e:
            raise EncryptionError(e) from e

    def decrypt(self, data: bytes, password: str) -> bytes:
        """
        解密
        输入: data: bytes, password: str
        输出: data: bytes
        """
        try:
            return self._crypto.decrypt(data, password)
        except ValueError as e:
            raise InvalidPasswordError(e)
        except Exception as e:
            raise DecryptionError(e) from e
