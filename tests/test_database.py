from database import DatabaseManager

def test_history_and_settings(tmp_path):
    db=DatabaseManager(tmp_path/'test.db'); db.add_history('user','Hello','greetings'); db.set_setting('history_enabled', True)
    assert db.history()[0][1] == 'Hello'; assert db.get_setting('history_enabled') == 'True'; db.close()
