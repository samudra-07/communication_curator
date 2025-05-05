# server.py
import socket
import threading
import nltk
from datetime import datetime
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tokenize.treebank import TreebankWordDetokenizer

# Ensure NLTK data is available
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

lemmatizer  = WordNetLemmatizer()
detokenizer = TreebankWordDetokenizer()

# Lemma → quirky replacements
replacements = {
    "stupid": "super-duper",
    "idiot": "inspiration",
    "dumb": "delightful",
    "hate": "heart-emoji",
    "suck": "sparkles",
    "ugly": "unique",
    "bad": "bodacious",
    "awful": "awesome-sauce",
    "terrible": "terrific",
    "horrible": "huggable",
    "hell": "heck",
    "damn": "darn",
    "crap": "candy"
}

# Global structures
clients   = set()                # all sockets
usernames = {}                   # sock → name
rooms     = {"General": set()}   # room → set(sockets)
history   = {"General": []}      # room → [(ts,user,text),...]
LOG_FILE  = "chat.log"
LOCK      = threading.Lock()

def log_message(ts, room, user, text):
    with LOCK, open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{ts} [{room}] {user}: {text}\n")

def broadcast_room(msg_bytes, room, exclude=None):
    for c in rooms.get(room, []):
        if c is not exclude:
            try:
                c.send(msg_bytes)
            except:
                _remove_client(c)

def _remove_client(sock):
    if sock in clients:
        clients.remove(sock)
    user = usernames.pop(sock, None)
    for r in rooms.values():
        r.discard(sock)
    sock.close()
    if user:
        notice = f"*** {user} has left the chat ***\n".encode()
        for room in rooms:
            broadcast_room(notice, room)

def handle_client(sock):
    try:
        name = sock.recv(1024).decode().strip()
        usernames[sock] = name
        clients.add(sock)
        rooms["General"].add(sock)
        broadcast_room(f"*** {name} joined General ***\n".encode(), "General", exclude=sock)
        sock.send(b"[Joined room: General]\n")
    except:
        _remove_client(sock)
        return

    while True:
        try:
            data = sock.recv(2048)
            if not data:
                break
            text = data.decode().strip()
            room = next(r for r, sset in rooms.items() if sock in sset)

            # Command handling
            if text.startswith("/"):
                parts = text.split(maxsplit=2)
                cmd = parts[0].lower()

                if cmd == "/who":
                    users = [usernames[c] for c in rooms[room]]
                    sock.send(f"Users in {room}: {', '.join(users)}\n".encode())

                elif cmd == "/join" and len(parts) > 1:
                    new = parts[1]
                    rooms.setdefault(new, set()).add(sock)
                    history.setdefault(new, [])
                    for r in rooms:
                        if r != new:
                            rooms[r].discard(sock)
                    sock.send(f"[Switched to room: {new}]\n".encode())

                elif cmd == "/history":
                    n = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 10
                    for ts, u, msg in history[room][-n:]:
                        sock.send(f"{ts} {u}: {msg}\n".encode())

                else:
                    sock.send(b"Unknown command. Use /who /join <room> /history <n>\n")
                continue

            # 1) Tokenize & replace inappropriate words
            toks = word_tokenize(text)
            out = []
            replaced = False
            for tok in toks:
                lemma = lemmatizer.lemmatize(tok.lower())
                if lemma in replacements:
                    rep = replacements[lemma]
                    # preserve capitalization
                    if tok[0].isupper():
                        rep = rep.capitalize()
                    out.append(rep)
                    replaced = True
                else:
                    out.append(tok)
            filtered = detokenizer.detokenize(out)

            # 2) If replacements happened, warn the sender
            if replaced:
                sock.send(b"[WARNING] Your message contained inappropriate words and was modified.\n")

            # 3) Broadcast the (possibly filtered) message
            ts  = datetime.now().strftime("[%H:%M]")
            msg = f"{ts} {usernames[sock]}: {filtered}\n"
            log_message(ts, room, usernames[sock], filtered)
            history[room].append((ts, usernames[sock], filtered))
            broadcast_room(msg.encode(), room, exclude=sock)

        except:
            break

    _remove_client(sock)

def start_server(host="127.0.0.1", port=12345):
    open(LOG_FILE, "w").close()
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.bind((host, port))
    srv.listen()
    print(f"[SERVER] Listening on {host}:{port}")
    while True:
        client_sock, _ = srv.accept()
        threading.Thread(target=handle_client, args=(client_sock,), daemon=True).start()

if __name__ == "__main__":
    start_server()
