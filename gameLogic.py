import random
from dataclasses import dataclass
import pandas as pd

EXCEL_FILE = "C1_English_App.xlsx"
xl = pd.ExcelFile(EXCEL_FILE)

@dataclass
class PhrasalVerb:
    phrasal_verb: str
    base_verb: str
    particle: str
    spanish: str

def pick_random_phrasal_verb(verbs: list[PhrasalVerb]) -> PhrasalVerb:
    return random.choice(verbs)


def load_verbs(sheet_name: str, ):
    if sheet_name is None:
        sheet_name = xl.sheet_names[0]
    df = pd.read_excel(EXCEL_FILE, sheet_name=sheet_name)
    verbs = []
    for _, row in df.iterrows():
        verbs.append(PhrasalVerb(
            phrasal_verb=str(row["Phrasal Verb"]).strip(),
            base_verb=str(row["Base Verb"]).strip(),
            particle=str(row["Particle / Preposition"]).strip(),
            spanish=str(row["Spanish Translation"]).strip(),
        ))
    return verbs


def check_particle(verb: PhrasalVerb, guess: str) -> bool:
    return guess.strip().lower() == verb.particle.lower()

def normalise(text: str) -> str:
    return " ".join(text.lower().split())

def full_phrasal_verb(verb: PhrasalVerb) -> str:
    return f"{verb.base_verb} {verb.particle}"