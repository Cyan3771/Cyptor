from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from .base import BaseCryptor


# AES实现
class CyptorAES(BaseCryptor):
    # 密钥生成
    def _generate_key(self, password: str, salt: bytes) -> bytes:
        """x
        生成密钥
        输入: password: str, salt: bytes
        输出: key: bytes
        """
        return PBKDF2(password, salt, dkLen=32, count=1_000_000, hmac_hash_module=SHA256)

    # 加密
    def encrypt(self, data: bytes, password: str) -> tuple[bytes, bytes, bytes]:
        """
        加密
        输入: data: bytes, password: str
        输出: salt: bytes, iv: bytes, encrypted_data: bytes
        """
        # 生成随机盐和IV
        salt = get_random_bytes(16)
        iv = get_random_bytes(16)

        # 生成密钥
        key = self._generate_key(password, salt)

        # 创建AES加密器
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # 填充数据并加密
        padded_data = pad(data, AES.block_size)
        encrypted_data = cipher.encrypt(padded_data)

        # 返回盐 + IV + 加密数据
        return (salt, iv, encrypted_data)

    # 解密
    def decrypt(self, salt: bytes, iv: bytes, encrypted_data: bytes, password: str) -> bytes:
        """
        解密
        输入: salt: bytes, iv: bytes, encrypted_data: bytes, password: str
        输出: data: bytes
        """
        # 生成密钥
        key = self._generate_key(password, salt)

        # 创建AES解密器
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # 解密并去除填充
        decrypted_padded_data = cipher.decrypt(encrypted_data)
        decrypted_data = unpad(decrypted_padded_data, AES.block_size)

        # 返回解密后的数据
        return decrypted_data
