from datetime import datetime
def current_time(): return datetime.now().strftime('%I:%M %p')
def current_date(): return datetime.now().strftime('%B %d, %Y')
