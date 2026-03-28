import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

os.makedirs("RSA_Keys", exist_ok=True)

def createRSAKey():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
        )

    public_key = private_key.public_key()

    with open("RSA_Keys/private.pem", "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    with open("RSA_Keys/public.pem", "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

if __name__ == '__main__':
    createRSAKey()