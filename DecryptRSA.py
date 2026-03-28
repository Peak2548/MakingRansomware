import os
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def decrypt_rsa(encrypted_file: str, private_key_file: str, output_file: str):
    with open(private_key_file, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    with open(encrypted_file, "rb") as f:
        encrypted = f.read()

    decrypted = private_key.decrypt(
        encrypted,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open(output_file, "wb") as f:
        f.write(decrypted)
    os.remove('master.key.enc')

if __name__ == '__main__':
    decrypt_rsa(encrypted_file='master.key.enc', private_key_file='private.pem', output_file='master.key'
    )