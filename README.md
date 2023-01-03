## Relays Monitor
A GUI made with tkinter and customtkinter.


### 📦 Installation

#### Manual
1. Create and activate a virtual enviroment:
```
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Execute the program:
```
python main.py
```
#### Automatic
```
sh run.sh
```


### 🗂️ Structure
```
.
├── README.md
├── gui
│   ├── __init__.py
│   ├── application.py   # The main logic
│   ├── settings.py      # Some global settings
│   ├── led.py           # A custom Led component
│   ├── logs.py          # A loguru logger
│   ├── navbar.py        # A custom navbar component
│   ├── pin.py           # A custom pin manager component
│   ├── recorder.py      # A custom time recorder
│   ├── relaybox.py      # A custom relaybox component
│   └── stopwatch.py     # A custom stopwatch component
└── main.py
```