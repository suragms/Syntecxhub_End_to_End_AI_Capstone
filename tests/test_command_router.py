from commands.command_router import CommandRouter
from commands.web_commands import google_search_url

def test_invalid_command_rejected(): assert not CommandRouter().execute('run_shell').success
def test_search_url_is_encoded(): assert google_search_url('python programming') == 'https://www.google.com/search?q=python+programming'
def test_web_command_uses_injected_browser():
    seen=[]; result=CommandRouter(browser_opener=lambda url: seen.append(url) or True).execute('search_google','ai')
    assert result.success and seen == ['https://www.google.com/search?q=ai']
def test_application_uses_argv():
    seen=[]; result=CommandRouter(process_runner=lambda args, shell: seen.append((args,shell))).execute('open_notepad')
    assert result.success and seen == [(['notepad.exe'], False)]
