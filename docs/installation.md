# Installation

On Windows 10/11 with Python 3.11 or newer:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
python -m pytest -v
```

PyAudio installation depends on the local Python/Windows audio driver combination. If it is unavailable, typed commands and all non-microphone features remain usable.
