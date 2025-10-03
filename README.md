# CCN

A minimal Bluetooth-based two-peer chat server and client implemented in Python.

Files
- `server.py` — Bluetooth server that accepts up to two clients and forwards messages between them.
- `CCN.py` — Bluetooth client that connects to the server and sends/receives messages.

Quick notes
- The code uses Python's `socket` module with Bluetooth constants (AF_BLUETOOTH / BTPROTO_RFCOMM).
- On many platforms (especially Windows), you may need an external Bluetooth library such as `PyBluez` for full support.
- Replace the hard-coded MAC address in both files before running (`F8:16:54:A5:2D:18` in the examples).

Prerequisites
- Python 3.8+ recommended.
- A Bluetooth adapter on the host running the server and on clients.
- Pairing between devices may be required depending on your OS and adapter.

Install

Open PowerShell and run:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Usage

1. Edit `server.py` and `CCN.py` and set the Bluetooth MAC address and RFCOMM channel to match your environment.

2. Start the server (run on the machine acting as the Bluetooth server):

```powershell
python server.py
```

You should see "Waiting for connections..." and then client connection messages.

3. Start the client on another device (or the same device if supported):

```powershell
python CCN.py
```

The client will print "Connected to the server!" and you can send messages. Type `over` on the client to yield sending to the other peer (the code uses a simple "take turns" mechanism).

Platform notes and troubleshooting
- Windows: native Bluetooth socket support in the Python stdlib is limited. If you see errors about AF_BLUETOOTH, install `pybluez` and run with an appropriate adapter driver.
- Linux: BlueZ provides robust support; the socket constants in the code are standard on Linux kernels with Bluetooth support.
- If connections fail, verify the MAC address, RFCOMM channel, and that your OS has granted the process permission to use Bluetooth hardware.

Security
- This project is a learning/demo prototype. Do not use this as-is for production communication. It lacks authentication and encryption.

License
- Add your preferred license here.

Contributing
- Feel free to open issues or send pull requests for improvements (cross-platform support, error handling, tests, etc.).

Acknowledgements
- Based on simple socket examples and RFCOMM usage patterns.