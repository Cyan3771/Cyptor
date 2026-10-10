from abc import ABC, abstractmethod


class BaseCrypto(ABC):
    """
    输入: data: bytes, password: str
    输出: data: bytes
    """
    @abstractmethod
    def encrypt(self, data: bytes, password: str) -> bytes:
        pass

    @abstractmethod
    def decrypt(self, data: bytes, password: str) -> bytes:
        pass
