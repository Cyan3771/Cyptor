from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os

from core.crypto.base import BaseCrypto


class ChaCha20(BaseCrypto):
    """ChaCha20实现"""

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
        # 统一生成盐和 IV
        salt = os.urandom(16)
        iv = os.urandom(16)
        key = self._derive_key(password, salt)

        # ChaCha20 加密
        cipher = Cipher(algorithms.ChaCha20(key, iv),
                        mode=None, backend=self.backend)
        encryptor = cipher.encryptor()
        encrypted = encryptor.update(data) + encryptor.finalize()

        # 统一输出格式
        return salt + iv + encrypted

    # 解密
    def decrypt(self, data: bytes, password: str) -> bytes:
        # 统一切割格式
        salt = data[:16]
        iv = data[16:32]
        encrypted = data[32:]

        key = self._derive_key(password, salt)

        # ChaCha20 解密
        cipher = Cipher(algorithms.ChaCha20(key, iv),
                        mode=None, backend=self.backend)
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(encrypted) + decryptor.finalize()

        return decrypted
