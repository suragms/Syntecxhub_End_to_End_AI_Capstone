from urllib.parse import quote_plus
from .command_validator import validate
from core.models import CommandResult
class CommandRouter:
    def __init__(self, process_runner=None, browser_opener=None): self.process_runner, self.browser_opener = process_runner, browser_opener
    def execute(self, command, argument=None):
        try: validate(command, argument)
        except ValueError as exc: return CommandResult(False, str(exc), command)
        try:
            if command.startswith('open_') and command not in {'open_google','open_youtube','open_github'}:
                return self._app(command)
            urls = {'open_google':'https://www.google.com','open_youtube':'https://www.youtube.com','open_github':'https://github.com'}
            url = urls.get(command) or f'https://www.google.com/search?q={quote_plus(argument)}'
            opener = self.browser_opener or __import__('webbrowser').open
            if not opener(url): return CommandResult(False, 'The browser could not open the requested page.', command)
            return CommandResult(True, 'Opened the requested page in your browser.', command)
        except Exception as exc: return CommandResult(False, f'Action failed: {exc}', command)
    def _app(self, command):
        import os, subprocess
        apps = {'open_notepad':['notepad.exe'], 'open_calculator':['calc.exe'], 'open_paint':['mspaint.exe'], 'open_explorer':['explorer.exe'], 'open_settings':['explorer.exe','ms-settings:']}
        args = apps[command]
        runner = self.process_runner or subprocess.Popen
        runner(args, shell=False)
        return CommandResult(True, f'Opened {command[5:].replace("_", " ").title()}.', command)
