# SURA AI — Smart Personal Assistant

**Syntecxhub Artificial Intelligence Internship · Task 4 Project 2**  
**Developer:** Surag M S  
**Platform:** Windows 10/11 · **Language:** Python 3.11+

SURA AI is a local desktop capstone combining OpenCV face detection, rule-based conversational intent matching, optional speech recognition, offline text-to-speech, safe Windows/web actions, and a PySide6 dashboard.

## What it does

- Opens a webcam and detects faces using OpenCV Haar cascades.
- Requires a stable single-face **presence** check before the assistant dashboard.
- Accepts typed commands and optional microphone speech.
- Answers greetings, help, time/date/day questions and assistant information requests.
- Launches only approved applications and validated websites/searches.
- Stores optional local command history/settings in SQLite.
- Keeps camera, speech, TTS, and command errors visible without taking down typed chat.

> **Important privacy and security note:** Face detection is not face recognition and is not proof of identity. The mandatory mode does not authenticate, enroll, or match people. SURA AI does not store face images, biometric templates, or microphone recordings.

## Installation and use

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

Run tests with:

```powershell
python -m pytest -v
```

See [docs/installation.md](docs/installation.md), [docs/commands.md](docs/commands.md), and [docs/demo_script.md](docs/demo_script.md).

## Architecture

`main.py` composes `core/assistant_controller.py`, `vision/`, `voice/`, `chatbot/`, `commands/`, `database/`, and `gui/`. The chatbot emits structured command IDs. The command router uses fixed argument lists and `shell=False`; arbitrary shell input is never executed. See [docs/architecture.md](docs/architecture.md).

## Limitations

Haar detection varies with lighting, pose, occlusion, and camera quality and can produce false positives/negatives. Speech recognition depends on microphone permissions, PyAudio, and its online provider. Windows voices and installed applications vary by machine. Performance and hardware results are not claimed unless measured on the target device. Optional LBPH identity recognition is intentionally deferred.

## Packaging

After installing PyInstaller, run `python scripts/build_windows.py`. The resulting executable should be manually tested on a clean Windows machine before distribution.

## License

MIT. See [LICENSE](LICENSE).
