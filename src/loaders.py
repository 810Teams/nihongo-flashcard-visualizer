'''
    `loaders.py`
'''

def load_default_style():
    ''' Function: Load default style '''
    try:
        return list(open('DEFAULT_STYLE.txt'))[0].replace('\n', '').strip()
    except (FileNotFoundError, IndexError):
        return None
        