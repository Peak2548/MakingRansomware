import socket
import os
import threading

HOST = '0.0.0.0'
PORT = 5001
DISCOVERY_PORT = 9999
SAVE_DIR = 'ReceivedFiles'

os.makedirs(SAVE_DIR, exist_ok=True)

# DISCOVERY
def discovery_server():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp.bind(('0.0.0.0', DISCOVERY_PORT))

    while True:
        data, addr = udp.recvfrom(1024)
        if data == b'FIND_SERVER':
            udp.sendto(b'SERVER_HERE', addr)

# RECV EXACT
def recv_exact(conn, size):
    data = b''
    while len(data) < size:
        chunk = conn.recv(size - len(data))
        if not chunk:
            return None
        data += chunk
    return data

def main():
    threading.Thread(target=discovery_server, daemon=True).start()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)

    print(f'Server Port: {PORT}')

    conn, addr = server.accept()
    print(f'Connected: {addr}')

    try:
        while True:
            mode_raw = recv_exact(conn, 16)
            if not mode_raw:
                break

            mode = mode_raw.decode().strip()

            # FILES
            if mode == 'FILES':
                total_files = int(recv_exact(conn, 16).decode().strip())

                for i in range(total_files):
                    header = recv_exact(conn, 1024).decode().strip()
                    filename, filesize = header.split('|')
                    filename = filename.replace('\\', os.sep)
                    filesize = int(filesize)

                    if filename == 'SKIP':
                        conn.send(b'SKIP')
                        continue

                    save_path = os.path.join(SAVE_DIR, filename)
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)

                    print(f"Sending: {filename}")

                    conn.send(b'SEND')

                    received = 0
                    with open(save_path, 'wb') as f:
                        while received < filesize:
                            chunk = conn.recv(min(4096, filesize - received))
                            if not chunk:
                                break
                            f.write(chunk)
                            received += len(chunk)

                    if received == filesize:
                        conn.send(b'OK')
                        print(f'Saved: {save_path}')
                    else:
                        conn.send(b'ERROR')

            # KEY
            elif mode == 'KEY':
                header = recv_exact(conn, 1024).decode().strip()
                filename, filesize = header.split('|')
                filesize = int(filesize)

                save_path = os.path.join(SAVE_DIR, filename)
                received = 0
                with open(save_path, 'wb') as f:
                    while received < filesize:
                        chunk = conn.recv(min(4096, filesize - received))
                        if not chunk:
                            break
                        f.write(chunk)
                        received += len(chunk)

                if received == filesize:
                    conn.send(b'OK')
                else:
                    conn.send(b'ERROR')

            else:
                print('Unknown mode')
                break

    except Exception as e:
        print(f'Error: {e}')

    finally:
        conn.close()
        server.close()


if __name__ == '__main__':
    main()