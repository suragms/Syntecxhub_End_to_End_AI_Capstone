import sqlite3
from pathlib import Path
from datetime import datetime
class DatabaseManager:
    def __init__(self, path=None):
        self.path = Path(path or Path.home() / 'AppData' / 'Local' / 'SuraAI' / 'sura_ai.db'); self.conn = None; self.enabled = True
        try: self._open()
        except sqlite3.Error: self.enabled = False
    def _open(self):
        self.path.parent.mkdir(parents=True, exist_ok=True); self.conn = sqlite3.connect(self.path)
        self.conn.executescript('CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL); CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY, role TEXT, content TEXT, intent TEXT, status TEXT, timestamp TEXT);'); self.conn.commit()
    def add_history(self, role, content, intent='', status=''):
        if self.enabled: self.conn.execute('INSERT INTO history(role,content,intent,status,timestamp) VALUES (?,?,?,?,?)',(role,content,intent,status,datetime.now().isoformat())); self.conn.commit()
    def history(self, limit=100):
        if not self.enabled: return []
        return self.conn.execute('SELECT role,content,intent,status,timestamp FROM history ORDER BY id DESC LIMIT ?', (limit,)).fetchall()[::-1]
    def get_setting(self, key, default=None):
        if not self.enabled: return default
        row = self.conn.execute('SELECT value FROM settings WHERE key=?',(key,)).fetchone(); return row[0] if row else default
    def set_setting(self, key, value):
        if self.enabled: self.conn.execute('INSERT OR REPLACE INTO settings(key,value) VALUES (?,?)',(key,str(value))); self.conn.commit()
    def clear_history(self):
        if self.enabled: self.conn.execute('DELETE FROM history'); self.conn.commit()
    def close(self):
        if self.conn: self.conn.close(); self.conn = None
