from cryptography.fernet import Fernet
from os import environ, path
from pathlib import Path


KEY_LOCATION_ENV = 'EASY_ENCRYPTION_KEY_LOCATION'


def get_key(location_key: str = None) -> str:
    """
    Return the key to encrypt and decrypt data
    """
    location_key = location_key or environ.get(
        KEY_LOCATION_ENV,
        path.join(Path.home(), 'easy_encryption.key')
    )
    if path.exists(location_key):
        with open(location_key, 'rb') as f:
            return f.read()
    else:
        key=Fernet.generate_key()
        with open(location_key, 'wb') as f:
            f.write(key)
        return key


class EasyEncryption:

    def __init__(self, location_key: str = None):
        self._fernet=Fernet(get_key(location_key))

    @ classmethod
    def encrypt(cls, message: str) -> str:
        """
        Encrypt a message
        """
        return cls()._fernet.encrypt(message.encode()).decode()

    @ classmethod
    def decrypt(cls, enc_msg: str) -> str:
        """
        Decrypt a message
        """
        return cls()._fernet.decrypt(enc_msg.encode()).decode()


if __name__ == '__main__':
    enc_msg=EasyEncryption.encrypt('Hello World!!!')
    print('Encrypt', enc_msg)
    print('Decrypt', EasyEncryption.decrypt(enc_msg))
