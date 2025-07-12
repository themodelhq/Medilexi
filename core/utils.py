
from fuzzywuzzy import fuzz

def fuzzy_match(input_text, target_text, threshold=70):
    return fuzz.partial_ratio(input_text.lower(), target_text.lower()) >= threshold
