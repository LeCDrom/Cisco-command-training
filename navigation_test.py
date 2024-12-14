import random
import re
import argparse
import pickle
from copy import deepcopy


# Virtual config file

global default_config
global running_config
global startup_config

default_config = {
        "hostname": "Switch",
}

running_config = {
        "hostname": "SW1",
}

startup_config = {
        "hostname": "Switch"
}

# =================================

def open_file(name: str) -> str:
    data = ""
    with open(name, 'r') as f:
        for line in f:
            data += line
    f.close()
    return data

global prompt
prompt = {
    "user": f"{running_config["hostname"]}> ",
    "privileged": f"{running_config["hostname"]}# ",
    "config": f"{running_config["hostname"]}(config)# ",
    "config if": f"{running_config["hostname"]}(config-if)# ",
    "config line": f"{running_config["hostname"]}(config-line)# "
}

def update_prompts(current: dict, modes: dict):
    global prompt
    prompt["user"] = f"{running_config['hostname']}> "
    prompt["privileged"] = f"{running_config['hostname']}# "
    prompt["config"] = f"{running_config['hostname']}(config)# "
    prompt["config if"] = f"{running_config['hostname']}(config-if)# "
    prompt["config line"] = f"{running_config['hostname']}(config-line)# "

    current["prompt"] = modes[current["mode"]]

# =================== Available commands ===================

def enable(current: dict, modes: dict, usr_input: str, args: str):
    if args == "":
        current["mode"] = "privileged"
        current["prompt"] = modes["privileged"]
        return
    else:
        print(f"% Syntaxe invalide: arguments inattendus ({args})")

def config_t(current: dict, modes: dict, usr_input: str, args: str):
    if usr_input.startswith("conf t") or usr_input.startswith("config t"):
        if args.strip() == "":
            current["mode"] = "config"
            current["prompt"] = modes["config"]
            return
        
        else:
            print(f"% Syntaxe invalide: arguments inattendus ({args})")
    
    elif usr_input.startswith("configure"):
        if args.strip() == "terminal" or args.strip() == "t":
            current["mode"] = "config"
            current["prompt"] = modes["config"]
            return
        
        else:
            print(f"% Syntaxe invalide: arguments inattendus ({args})")

def exit_mode(current: dict, modes: dict, usr_input: str, args: str):
    if args == "":
        if current["mode"] in ("user", "privileged"):
            current["mode"] = "user"
            current["prompt"] = modes["user"]
        
        elif current["mode"] == "config":
            current["mode"] = "privileged"
            current["prompt"] = modes["privileged"]
        
        elif current["mode"] in ("config if", "config line"):
            current["mode"] = "config"
            current["prompt"] = modes["config"]
        return
    else:
        print(f"% Syntaxe invalide: arguments inattendus ({args})")

def end(current: dict, modes: dict, usr_input: str, args: str):
    if args == "":
        current["mode"] = "privileged"
        current["prompt"] = modes["privileged"]
        return
    else:
        print(f"% Syntaxe invalide: arguments inattendus ({args})")

def show(current: dict, modes: dict, usr_input: str, args: str):
    pass

def write(current: dict, modes: dict, usr_input: str, args: str):
    global startup_config, running_config
    if args == "":
        startup_config = deepcopy(running_config)
        print("\n% Configuration sauvegardée dans la NVRAM\n")
    elif args == "erase":
        startup_config = deepcopy(default_config)
        print("\n% Configuration effacée de la NVRAM\n")
    else:
        print(f"\n% Syntaxe invalide: arguments inattendus ({args})\n")

def copy(current: dict, modes: dict, usr_input: str, args: str):
    global startup_config, running_config
    if args == "running-config startup-config":
        write(current, modes, usr_input, "")
    elif args == "startup-config running-config":
        running_config = deepcopy(startup_config)
        update_prompts(current, modes)
        print("\n% Configuration restaurée depuis la NVRAM\n")

def reload_sw(current: dict, modes: dict, usr_input: str, args: str):
    global startup_config, running_config
    if args == "":
        running_config = deepcopy(startup_config)
        update_prompts(current, modes)
        print("\n######################### Switch redémarré #########################\n")
    
    else:
        print(f"\n% Syntaxe invalide: arguments inattendus ({args})\n")

def help(current: dict, modes: dict, usr_input: str, args: str):
    if args == "":
        print("\nCommandes EXEC :")
        for cmd, desc in commands_list[current["mode"]].items():
            space = 15-len(cmd)
            print(f"  {cmd}{" "*space}{desc["description"]}")
        print()
    else:
        print(f"\n% Syntaxe invalide: arguments inattendus ({args})\n")

def ping(current: dict, modes: dict, usr_input: str, args: str):
    pass

def traceroute(current: dict, modes: dict, usr_input: str, args: str):
    pass

def no(current: dict, modes: dict, usr_input: str, args: str):
    pass

def interface(current: dict, modes: dict, usr_input: str, args: str):
    if args == "":
        current["mode"] = "config if"
        current["prompt"] = modes["config if"]
        return
    else:
        print(f"\n% Syntaxe invalide: arguments inattendus ({args})\n")

def hostname(current: dict, modes: dict, usr_input: str, args: str):
    global startup_config, running_config
    if args != "":
        running_config["hostname"] = args

        update_prompts(current, modes)

    else:
        print("\n% Argument attendu\n")

def username(current: dict, modes: dict, usr_input: str, args: str):
    pass

def crypto(current: dict, modes: dict, usr_input: str, args: str):
    pass

def line(current: dict, modes: dict, usr_input: str, args: str):
    current["mode"] = "config line"
    current["prompt"] = modes["config line"]
    return current

def enable_password(current: dict, modes: dict, usr_input: str, args: str):
    pass

def banner(current: dict, modes: dict, usr_input: str, args: str):
    pass

def service(current: dict, modes: dict, usr_input: str, args: str):
    pass

def spanning_tree(current: dict, modes: dict, usr_input: str, args: str):
    pass

def duplex(current: dict, modes: dict, usr_input: str, args: str):
    pass

def speed(current: dict, modes: dict, usr_input: str, args: str):
    pass

def descript(current: dict, modes: dict, usr_input: str, args: str):
    pass

def shutdown(current: dict, modes: dict, usr_input: str, args: str):
    pass

def switchport(current: dict, modes: dict, usr_input: str, args: str):
    pass

def password(current: dict, modes: dict, usr_input: str, args: str):
    pass

def login(current: dict, modes: dict, usr_input: str, args: str):
    pass

def transport(current: dict, modes: dict, usr_input: str, args: str):
    pass

def exec_timeout(current: dict, modes: dict, usr_input: str, args: str):
    pass

# =================== ------------------ ===================


def handle_commands(usr_input: str, modes: dict, current: dict) -> tuple:
    """
    Handles the navigation between terminal modes
    - usr_input : user navigation command
    - current : current mode and prompt text
    - modes : all modes and their prompts
    """
    mode = current["mode"]

    for cmd, details in commands_list[mode].items():
        
        if usr_input.startswith(cmd):
            try:
                details["handler"]
            except KeyError:
                print("\n% Aucun fonction associée pour le moment\n")
            else:
                args = usr_input[len(cmd):].strip()
                details["handler"](current, modes, usr_input, args)
            return

    print("\n% Commande inconnue ou non disponible dans ce mode\n")


# ===================== Commands list =====================

global commands_list
commands_list = {
        "user": {
            "enable": {"description": "Passer en mode privilégié ⤒", "negate": False, "handler": enable},
            "en": {"description": "Passer en mode privilégié ⤓", "negate": False, "handler": enable},
            "exit": {"description": "Retourner au mode précédent", "negate": False, "handler": exit_mode},
            "?": {"description": "Affiche les commandes disponibles dans le mode actuel", "negate": False, "handler": help}
        },
        
        "privileged": {
            "configure": {"description": "Passer en mode configuration terminal ⤒", "negate": False, "handler": config_t},
            "config t": {"description": "Passer en mode configuration terminal", "negate": False, "handler": config_t},
            "conf t": {"description": "Passer en mode configuration terminal ⤓", "negate": False, "handler": config_t},
            "show": {"description": "Afficher diverses informations sur les interfaces ⤒", "negate": False, "nohandler": show},
            "sh": {"description": "Afficher diverses informations sur les interfaces ⤓", "negate": False, "nohandler": show},
            "write": {"description": "Sauvegarder / supprimer configuration dans la NVRAM (mémoire non volatile) ⤒", "negate": False, "handler": write},
            "wr": {"description": "Sauvegarder / supprimer configuration dans la NVRAM (mémoire non volatile) ⤓", "negate": False, "handler": write},
            "copy": {"description": "Copier fichier vers destination", "negate": False, "handler": copy},
            "reload": {"description": "Redémarrer l'équipement", "negate": False, "handler": reload_sw},
            "ping": {"description": "Requête ping vers destination", "negate": False, "nohandler": ping},
            "traceroute": {"description": "Afficher parcours du paquet ICMP (hops)", "negate": False, "nohandler": traceroute},
            "no": {"description": "Inverser une commande", "negate": False, "handler": no},
            "exit": {"description": "Retourner au mode précédent", "negate": False, "handler": exit_mode},
            "?": {"description": "Affiche les commandes disponibles dans le mode actuel", "negate": False, "handler": help}
        },
        
        "config": {
            "interface": {"description": "Configurer les interfaces", "negate": False, "handler": interface},
            "hostname": {"description": "Configurer nom de l'équipement", "negate": True, "handler": hostname},
            "username": {"description": "Configurer utilisateurs", "negate": True, "nohandler": username},
            "crypto" : {"description": "Créer les clés de chiffrement", "negate": False, "nohandler": crypto},
            "line": {"description": "Configurer lignes X à Y", "negate": False, "handler": line},
            "enable": {"description": "Définir le mot passe du mode privilégié", "negate": False, "nohandler": enable_password},
            "banner": {"description": "Ajouter une bannière (message)", "negate": True, "nohandler": banner},
            "service": {"description": "Paramétrer, désactiver services", "negate": True, "nohandler": service},
            "spanning-tree": {"description": "Activer le spanning-tree (STP)", "negate": True, "nohandler": spanning_tree},
            "no": {"description": "Inverser une commande", "negate": False, "nohandler": no},
            "exit": {"description": "Retourner au mode précédent", "negate": False, "handler": exit_mode},
            "end": {"description": "Retourner au mode privilégié", "negate": False, "handler": end},
            "?": {"description": "Affiche les commandes disponibles dans le mode actuel", "negate": False, "handler": help}
        },

        "config if": {
            "duplex": {"description": "Définir le mode de transmission [ auto | half | full ]", "negate": False, "nohandler": duplex},
            "speed": {"description": "Définir la vitesse de transmission [ auto | 10 | 100 ]", "negate": False, "nohandler": speed},
            "description": {"description": "Établir la description de l'interface", "negate": True, "nohandler": descript},
            "shutdown": {"description": "Éteindre / désactiver l'interface", "negate": True}, "nohandler": shutdown,
            "switchport": {"description": "Configurer le type de port", "negate": False, "nohandler": switchport},
            "no": {"description": "Inverser une commande", "negate": False, "handler": no},
            "exit": {"description": "Retourner au mode précédent", "negate": False, "handler": exit_mode},
            "end": {"description": "Retourner au mode privilégié", "negate": False, "handler": end},
            "?": {"description": "Affiche les commandes disponibles dans le mode actuel", "negate": False, "handler": help}
        },

        "config line": {
            "password": {"description": "Définir un mot de passe", "negate": True, "nohandler": password},
            "login": {"description": "Activer authentification", "negate": True, "nohandler": login},
            "transport": {"description": "Activer authentification", "negate": True, "nohandler": transport},
            "exec-timeout": {"description": "Définir un timeout pour le mode privilégié *min* *sec*", "negate": True, "nohandler": exec_timeout},
            "no": {"description": "Inverser une commande", "negate": False, "nohandler": no},
            "exit": {"description": "Retourner au mode précédent", "negate": False, "handler": exit_mode},
            "end": {"description": "Retourner au mode privilégié", "negate": False, "handler": end},
            "?": {"description": "Affiche les commandes disponibles dans le mode actuel", "negate": False, "handler": help}
        }
}

# ===================== ------------- =====================


current_mode = {"mode": "user", "prompt": prompt["user"]}


while True:
    user_input = input(current_mode["prompt"])
    
    handle_commands(user_input, prompt, current_mode)
