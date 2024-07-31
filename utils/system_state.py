from dotenv import load_dotenv
from utils import coloration
import os
import json

load_dotenv('envs/.static.env')
etat_systeme_file = os.getenv("ETAT_SYSTEME")


def check_system(to_check: str):
    with open(etat_systeme_file, 'r') as f:
        etat_systeme = json.load(f)
    return etat_systeme[to_check]


def update_system(to_update: str):
    with open(etat_systeme_file, 'r') as f:
        etat_systeme = json.load(f)
    etat_systeme[to_update] = not etat_systeme[to_update]
    with open(etat_systeme_file, 'w') as f:
        json.dump(etat_systeme, f)
    coloration.print_info(f"{to_update} mis à jour")
