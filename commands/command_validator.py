ALLOWED = {'open_notepad','open_calculator','open_paint','open_explorer','open_settings','open_google','open_youtube','open_github','search_google','logout','exit','stop_listening'}
def validate(command, argument=None):
    if command not in ALLOWED: raise ValueError(f'Unsupported command: {command}')
    if command == 'search_google' and not argument: raise ValueError('Search text is required')
    return command, argument
