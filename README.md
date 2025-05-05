
# Communication Curator

**Communication Curator** is a Python-based chat server designed to foster positive communication in real-time chat rooms. The server implements NLP techniques to filter inappropriate language, replacing it with friendlier alternatives, and provides robust multi-room chat functionality.

## Features

* **Real-Time Chat:** Users can communicate in designated chat rooms with minimal latency.
* **Language Moderation:** Automatic detection and replacement of inappropriate words with positive alternatives using NLTK.
* **Room Management:**

  * Join existing chat rooms or create new ones.
  * Switch between chat rooms seamlessly.
* **User Commands:** Intuitive commands for users to:

  * View members in the current room (`/who`).
  * Retrieve chat history (`/history <n>`).
  * Join or switch chat rooms (`/join <room>`).
* **Chat Logging:** All messages are logged with timestamps for auditing or debugging.
* **Scalable Architecture:** Handles multiple users and rooms efficiently using threading.

## How It Works

1. **NLP-Based Moderation:**

   * Tokenizes messages using NLTK's `word_tokenize`.
   * Replaces inappropriate words (as defined in the `replacements` dictionary) with quirky, friendly alternatives while preserving capitalization.
   * Sends a warning to the sender if their message was modified.

2. **Room and User Management:**

   * Maintains separate message histories for each room.
   * Tracks active users and their associated sockets.
   * Notifies users when someone joins or leaves a room.

3. **Commands:**

   * `/who`: Lists all users in the current room.
   * `/join <room>`: Joins or creates a new room.
   * `/history <n>`: Displays the last `n` messages from the current room.

## Installation

### Prerequisites

* Python 3.x
* Required libraries: Install via pip.

  ```bash
  pip install -r requirements.txt
  ```

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/samudra-07/communication_curator.git
   cd communication_curator
   ```

2. Install NLTK data files (automatically handled in the script).

3. Start the server:

   ```bash
   python server.py
   ```

## Usage

1. **Starting the Server:**

   * The server will listen on `127.0.0.1:12345` by default.
   * Modify the `start_server` function if you need to customize the host or port.

2. **Connecting as a Client:**

   * Use any TCP client to connect (e.g., `telnet`).
   * Example:

     ```bash
     telnet 127.0.0.1 12345
     ```

3. **Interacting:**

   * Provide a username upon connection.
   * Use the commands (`/who`, `/join`, `/history`) or send messages directly.

## Example Session

* User joins the "General" room:

  ```
  *** John joined General ***
  [Joined room: General]
  ```

* User sends a message containing filtered words:

  ```
  John: This is so dumb!
  [WARNING] Your message contained inappropriate words and was modified.
  [12:30] John: This is so delightful!
  ```

* User switches to a new room:

  ```
  /join StudyGroup
  [Switched to room: StudyGroup]
  ```

* User views the last 5 messages:

  ```
  /history 5
  [12:25] Alice: Hello everyone!
  [12:26] Bob: Let's study together.
  ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to fork the repository, create a feature branch, and submit a pull request.

---

This README provides a comprehensive overview of the project, its features, and its usage instructions. Let me know if you’d like further refinements!
