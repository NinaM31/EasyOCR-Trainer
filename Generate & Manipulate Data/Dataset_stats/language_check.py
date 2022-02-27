import re
p = re.compile('^[\u0621-\u064A\u0660-\u0669]+$')


def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True
    
    
def isArabic(s):
    if p.match(s):
        return True
    return False


def check_language(text):
    text = str(text)
    if isEnglish(text):
        return 'English'
    
    if isArabic(text):
        return 'Arabic'
    return 'Mixed'