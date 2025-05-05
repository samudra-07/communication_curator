# client.py
import socket
import threading

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(2048).decode()
            if not msg:
                break
            print(msg, end='')
        except:
            break

def send_messages(sock):
    while True:
        try:
            line = input()
            sock.send(line.encode())
        except:
            break

def start_client(host='127.0.0.1', port=12345):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    username = input("Enter your username: ").strip()
    sock.send(username.encode())

    print(f"[CONNECTED] Welcome, {username}! Type messages and hit Enter.")
    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()
    send_messages(sock)
    sock.close()

if __name__ == "__main__":
    start_client()
