import re
import string


#The set of punctuations that will be cleaned out in labels
arabic_punctuations = '''`÷×؛_()^][ـ,:،/",'{}~¦+|”…“–ـ!'''
english_punctuations = "\"#'()+,-/;:!\[\\]^_`{|}~€"
punctuations_list = arabic_punctuations + english_punctuations

#Diacritics that will be cleaned if present in labels
arabic_diacritics = re.compile("""
                             ّ    | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida
                         """, re.VERBOSE)


def normalize_arabic(text):
    text = re.sub("[إأآا]", "ا", text)
    return text


def remove_diacritics(text):
    text = re.sub(arabic_diacritics, '', text)
    return text


def remove_punctuations(text):
    translator = str.maketrans('', '', punctuations_list)
    return text.translate(translator)


def clean_text(text):
    text = normalize_arabic(text)
    text = remove_punctuations(text)
    text = remove_diacritics(text)
    return text