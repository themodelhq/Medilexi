
from core.utils import fuzzy_match
import json
import os

SYMPTOM_DB_PATH = os.path.join("data", "symptoms.json")

def get_possible_conditions(user_input):
    with open(SYMPTOM_DB_PATH, "r", encoding="utf-8") as f:
        symptom_map = json.load(f)

    found = []
    for key, conditions in symptom_map.items():
        if fuzzy_match(user_input, key):
            found.extend(conditions)

    return list(set(found)) if found else ["Unknown - refer to clinician"]
