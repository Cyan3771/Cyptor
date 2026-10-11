from abc import ABC, abstractmethod


class BaseCryptor(ABC):
    """加密器抽象基类"""

    @abstractmethod
    def encrypt(self, data: bytes, password: str) -> tuple[bytes, bytes, bytes]:
        """
        加密
        输入: data: bytes, password: str
        输出: salt, iv, encrypted_data
        """
        ...

    @abstractmethod
    def decrypt(self, salt: bytes, iv: bytes, encrypted_data: bytes, password: str) -> bytes:
        """
        解密
        输入: salt, iv, encrypted_data, password
        输出: data: bytes
        """
        ...
