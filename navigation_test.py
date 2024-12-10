import random
from pyparsing import Word, alphas, nums, Literal, Optional, Combine, Regex
import argparse
import pickle


def open_file(name: str) -> str:
    data = ""
    with open(name, 'r') as f:
        for line in f:
            data += line
    f.close()
    return data

def get_key_from_value(data: dict):
    key_list = list(data.keys())
    val_list = list(data.values())


modes = {
        "user": {
            "enable": {"description": "Passer en mode privilégié", "negate": False}
        },
        
        "privileged": {
            "configure terminal": {"description": "Passer en mode configuration terminal", "negate": False},
            "config t": {"description": "Passer en mode privilégié"},
            "show": {"description": "Afficher diverses informations sur les interfaces", "negate": False},
            "write": {"description": "Sauvegarder configuration dans la NVRAM (mémoire non volatile)", "negate": False},
            "write erase": {"description": "Effacer fichier de configuration", "negate": False},
            "copy": {"description": "Copier fichier vers destination", "negate": False},
            "reload": {"description": "Redémarrer l'équipement", "negate": False},
            "terminal monitor": {"description": "Activer / désactiver les messages debug du terminal", "negate": True},
            "ping": {"description": "Requête ping vers destination", "negate": False},
            "traceroute": {"description": "Afficher parcours du paquet ICMP (hops)", "negate": False},
            "exit": {"description": "Retourner au mode précédent", "negate": False},
            "end": {"description": "Retourner au mode utilisateur", "negate": False}
        },
        
        "config": {
            "interface": {"description": "Configurer les interfaces"},
            "hostname": {"description": "Configurer nom de l'équipement", "negate": True},
            "username": {"description": "Configurer nom d'utilisateur", "negate": True},
            "crypto" : {"description": "Créer les clés de chiffrement", "negate": False},
            "line": {"description": "Configurer lignes X à Y", "negate": False},
            "enable": {"description": "Définir le mot passe du mode privilégié", "negate": False},
            "banner": {"description": "Ajouter une bannière (message)", "negate": True},
            "service": {"description": "Paramétrer, désactiver services", "negate": True},
            "spanning-tree": {"description": "Activer le spanning-tree (STP)", "negate": True}
        },

        "config if": {
            "duplex": {"description": "Définir le mode de transmission [ auto | half | full ]", "negate": False},
            "speed": {"description": "Définir la vitesse de transmission [ auto | 10 | 100 ]", "negate": False},
            "description": {"description": "Établir la description de l'interface", "negate": True},
            "shutdown": {"description": "Éteindre / désactiver l'interface", "negate": True}
        }
}

global interface
interface = Literal('interface') + Word(alphas + nums + "/-")
global ip
ip = Regex(r'\d+\.\d+\.\d+\.\d+')
global mask
mask = Regex(r'\d+\.\d+\.\d+\.\d+')
global ip_command
ip_command = Literal('ip address') + ip + mask

global command
command = interface | ip_command

hostname = "Equipment"

nav = {
    "user": f"{hostname}> ",
    "privileged": f"{hostname}# ",
    "config": f"{hostname}(config)# ",
    "config if": f"{hostname}(config-if)# "
    }

current_mode = {"name": "user", "prompt": nav["user"]}

while True:
    user_input = input(current_mode["prompt"])
    
    match current_mode["name"]:
        case "user":
            if user_input == "enable":
                current_mode["name"] = "privileged"
                current_mode["prompt"] = nav["privileged"]

        case "privileged":
            if user_input == "config t" or user_input == "configure terminal":
                current_mode["name"] = "config"
                current_mode["prompt"] = nav["config"]
            elif user_input == "exit" or user_input == "end":
                current_mode["name"] = "user"
                current_mode["prompt"] = nav["user"]

        case "config":
            if user_input == "interface":
                current_mode["name"] = "config if"
                current_mode["prompt"] = nav["config if"]
            elif user_input == "exit":
                current_mode["name"] = "privileged"
                current_mode["prompt"] = nav["privileged"]
            elif user_input == "end":
                current_mode["name"] = "user"
                current_mode["prompt"] = nav["user"]

        case "config if":
            if user_input == "exit":
                current_mode["name"] = "config"
                current_mode["prompt"] = nav["config"]
            elif user_input == "end":
                current_mode["name"] = "user"
                current_mode["prompt"] = nav["user"]
