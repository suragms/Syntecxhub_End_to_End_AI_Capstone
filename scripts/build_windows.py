from pathlib import Path
import PyInstaller.__main__
root = Path(__file__).resolve().parents[1]
PyInstaller.__main__.run(['--noconfirm','--clean','--name','SuraAI','--windowed','--add-data',f'{root / "chatbot" / "intents.json"};chatbot','main.py'])
