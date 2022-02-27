import pandas as pd


def get_strings_from_txt(path):
    f = open(path, 'r', encoding="utf8")
    results = []
    for l in f.readlines():
        if l and l.strip():
            results.append(l.strip())
            
    strings = [ get_display(arabic_reshaper.reshape(str(w))) for w in results ]
    return strings


def get_strings_from_csv(path):
    if isinstance(path, str):
        df = pd.read_csv(path)
    else:
        df = path
        
    words =list(df.words)
    strings = [ str(w) for w in words ]
    return strings