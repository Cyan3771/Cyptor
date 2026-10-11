from core.crypto.AES import CyptorAES
from core.crypto.base import BaseCryptor
from core.debug import CyptorError, ErrorCode


class CryptoManager:
    """加密管理器"""

    _ALGORITHM_REGISTRY: dict[str, type[BaseCryptor]] = {
        "AES-256-CBC": CyptorAES,
    }

    def __init__(self, algorithm: str):
        if algorithm not in self._ALGORITHM_REGISTRY:
            raise CyptorError(ErrorCode.ALGORITHM_NOT_SUPPORTED, params={
                              "algorithm": algorithm}, message=f"Algorithm not supported: {algorithm}")

        self._crypto: BaseCryptor = self._ALGORITHM_REGISTRY[algorithm]()

    def encrypt(self, data: bytes, password: str) -> tuple[bytes, bytes, bytes]:
        try:
            result = self._crypto.encrypt(data, password)
        except Exception as e:
            raise CyptorError(ErrorCode.ENCRYPT_FAILED, message=f"Encryption failed", debug={
                              "exception": str(e)})
        return result

    def decrypt(self, salt: bytes, iv: bytes, encrypted_data: bytes, password: str) -> bytes:
        try:
            result = self._crypto.decrypt(salt, iv, encrypted_data, password)
        except Exception as e:
            raise CyptorError(ErrorCode.DECRYPT_FAILED, message=f"Decryption failed", debug={
                              "exception": str(e)})
        return result
