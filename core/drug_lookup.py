
import json
import os
from core.utils import fuzzy_match

DRUG_DB_PATH = os.path.join("data", "drugs.json")

def lookup_drug(name):
    with open(DRUG_DB_PATH, "r", encoding="utf-8") as f:
        drug_data = json.load(f)

    for drug in drug_data:
        if fuzzy_match(name, drug):
            return drug_data[drug]

    return {"error": "Drug not found"}
