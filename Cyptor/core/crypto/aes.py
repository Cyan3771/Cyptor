from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

from core.crypto.base import BaseCrypto


class AES(BaseCrypto):
    """AES-256-CBC实现"""

    def __init__(self):
        self.backend = default_backend()

    # 密钥推导
    def _derive_key(self, password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return kdf.derive(password.encode())

    # 加密

    def encrypt(self, data: bytes, password: str) -> bytes:
        # 生成盐和IV
        salt = os.urandom(16)
        iv = os.urandom(16)
        key = self._derive_key(password, salt)

        # AES加密
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), self.backend)
        encryptor = cipher.encryptor()

        # PKCS7填充
        pad_len = 16 - len(data) % 16
        data += bytes([pad_len]) * pad_len
        encrypted = encryptor.update(data) + encryptor.finalize()

        # 输出
        return salt + iv + encrypted

    # 解密
    def decrypt(self, data: bytes, password: str) -> bytes:
        # 切割
        salt = data[:16]
        iv = data[16:32]
        encrypted = data[32:]

        key = self._derive_key(password, salt)

        # AES解密
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), self.backend)
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(encrypted) + decryptor.finalize()

        # 去填充
        pad_len = decrypted[-1]
        return decrypted[:-pad_len]
