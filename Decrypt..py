from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import os

KEY_FILE = 'master.key'

# LOAD KEY
def load_key():
    if not os.path.exists(KEY_FILE):
        print('No file: master.key')
        return None
    with open(KEY_FILE, 'rb') as f:
        return f.read()

# FILE DECRYPT
def decrypt_file(filepath, fernet):
    try:
        with open(filepath, 'rb') as f:
            encrypted_data = f.read()

        decrypted_data = fernet.decrypt(encrypted_data)

        if filepath.endswith('.enc'):
            output_path = filepath[:-4]
        else:
            output_path = filepath + '.dec'

        if os.path.exists(output_path):
            output_path += '.decrypted'

        with open(output_path, 'wb') as f:
            f.write(decrypted_data)

        os.remove(filepath)

    except Exception as e:
        print(e)


def decrypt_all():
    key = load_key()
    if not key:
        return

    fernet = Fernet(key)
    base_dir = os.path.dirname(os.path.abspath(__file__))

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.enc'):
                full_path = os.path.join(root, file)
                decrypt_file(full_path, fernet)


if __name__ == '__main__':
    decrypt_all()