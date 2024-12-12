import random
import re
import argparse
import pickle


def open_file(name: str) -> str:
    data = ""
    with open(name, 'r') as f:
        for line in f:
            data += line
    f.close()
    return data

# =================== Available commands ===================

def enable(current: dict, modes: dict, usr_input: str, args: str):
    if args == "":
        current["mode"] = "privileged"
        current["prompt"] = modes["privileged"]
        return current
    else:
        print(f"% Syntaxe invalide ({args})")

def config_t(current: dict, modes: dict, usr_input: str, args: str):
    """if usr_input.startswith("config t") or usr_input.startswith("configure terminal"):
        if args.strip() == "":
            current["mode"] = "config"
            current["prompt"] = modes["config"]
            return current
        else:
            print(f"% Syntaxe invalide ({args})")"""
    mode = current["mode"]

    for cmd, details in commands_list[mode].items():
        match = re.match(f"^{cmd}(.*)", usr_input)
        if match:
            args = match.group(1).strip()
            details["handler"](current, modes, usr_input, args)
            return

    print("% Commande invalide ou non disponible dans ce mode")

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
        return current
    else:
        print(f"% Syntaxe invalide ({args})")

def end(current: dict, modes: dict, usr_input: str, args: str):
    if args == "":
        current["mode"] = "privileged"
        current["prompt"] = modes["privileged"]
        return current
    else:
        print(f"% Syntaxe invalide ({args})")

def show(current: dict, modes: dict, usr_input: str, args: str):
    pass

def write(current: dict, modes: dict, usr_input: str, args: str):
    if args == "":
        pass
    else:
        print(f"% Syntaxe invalide ({args})")

def copy(current: dict, modes: dict, usr_input: str, args: str):
    pass

def reload_sw(current: dict, modes: dict, usr_input: str, args: str):
    if args == "":
        pass
    else:
        print(f"% Syntaxe invalide ({args})")

def mode_monitor(current: dict, modes: dict, usr_input: str, args: str):
    if args == "":
        pass
    else:
        print(f"% Syntaxe invalide ({args})")

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
        return current
    else:
        print(f"% Syntaxe invalide ({args})")

def hostname(current: dict, modes: dict, usr_input: str, args: str):
    pass

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

def description(current: dict, modes: dict, usr_input: str, args: str):
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


def handle_commands(usr_input: str, current: dict, modes: dict) -> tuple:
    """
    Handles the navigation between terminal modes
    - usr_input : user navigation command
    - current : current mode and prompt text
    - modes : all modes and their prompts
    """
    mode = current["mode"]
    prefix = usr_input.split()[0]

    for cmd, details in commands_list[mode].items():
        if usr_input.startswith(cmd):
            args = usr_input[len(cmd):].strip()
            details["handler"](current, modes, usr_input, args)
            return

    # Check for partial matches
    for cmd, details in commands_list[mode].items():
        if cmd.startswith(prefix):
            print(f"Did you mean '{cmd}'?")
            return

    print("% Commande invalide ou non disponible dans ce mode")


# ===================== Commands list =====================

global commands_list
commands_list = {
        "user": {
            "enable": {"description": "Passer en mode privilégié", "negate": False, "handler": enable},
            "exit": {"description": "Retourner au mode précédent", "negate": False, "handler": exit_mode}
        },
        
        "privileged": {
            "configure terminal": {"description": "Passer en mode configuration terminal", "negate": False, "handler": config_t},
            "config t": {"description": "Passer en mode privilégié", "negate": False, "handler": config_t},
            "show": {"description": "Afficher diverses informations sur les interfaces", "negate": False, "nohandler": show},
            "write": {"description": "Sauvegarder / supprimer configuration dans la NVRAM (mémoire non volatile)", "negate": False, "nohandler": write},
            "copy": {"description": "Copier fichier vers destination", "negate": False, "nohandler": copy},
            "reload": {"description": "Redémarrer l'équipement", "negate": False, "nohandler": reload_sw},
            "terminal monitor": {"description": "Activer / désactiver les messages debug du terminal", "negate": True, "nohandler": mode_monitor},
            "ping": {"description": "Requête ping vers destination", "negate": False, "nohandler": ping},
            "traceroute": {"description": "Afficher parcours du paquet ICMP (hops)", "negate": False, "nohandler": traceroute},
            "no": {"description": "Inverser une commande", "negate": False, "handler": no},
            "exit": {"description": "Retourner au mode précédent", "negate": False, "handler": exit_mode}
        },
        
        "config": {
            "interface": {"description": "Configurer les interfaces", "negate": False, "handler": interface},
            "hostname": {"description": "Configurer nom de l'équipement", "negate": True, "nohandler": hostname},
            "username": {"description": "Configurer utilisateurs", "negate": True, "nohandler": username},
            "crypto" : {"description": "Créer les clés de chiffrement", "negate": False, "nohandler": crypto},
            "line": {"description": "Configurer lignes X à Y", "negate": False, "handler": line},
            "enable": {"description": "Définir le mot passe du mode privilégié", "negate": False, "nohandler": enable_password},
            "banner": {"description": "Ajouter une bannière (message)", "negate": True, "nohandler": banner},
            "service": {"description": "Paramétrer, désactiver services", "negate": True, "nohandler": service},
            "spanning-tree": {"description": "Activer le spanning-tree (STP)", "negate": True, "nohandler": spanning_tree},
            "no": {"description": "Inverser une commande", "negate": False, "nohandler": no},
            "exit": {"description": "Retourner au mode précédent", "negate": False, "handler": exit_mode},
            "end": {"description": "Retourner au mode privilégié", "negate": False, "handler": end}
        },

        "config if": {
            "duplex": {"description": "Définir le mode de transmission [ auto | half | full ]", "negate": False, "nohandler": duplex},
            "speed": {"description": "Définir la vitesse de transmission [ auto | 10 | 100 ]", "negate": False, "nohandler": speed},
            "description": {"description": "Établir la description de l'interface", "negate": True, "nohandler": description},
            "shutdown": {"description": "Éteindre / désactiver l'interface", "negate": True}, "nohandler": shutdown,
            "switchport": {"description": "Configurer le type de port", "negate": False, "nohandler": switchport},
            "no": {"description": "Inverser une commande", "negate": False, "handler": no},
            "exit": {"description": "Retourner au mode précédent", "negate": False, "handler": exit_mode},
            "end": {"description": "Retourner au mode privilégié", "negate": False, "handler": end}
        },

        "config line": {
            "password": {"description": "Définir un mot de passe", "negate": True, "nohandler": password},
            "login": {"description": "Activer authentification", "negate": True, "nohandler": login},
            "transport": {"description": "Activer authentification", "negate": True, "nohandler": transport},
            "exec-timeout": {"description": "Définir un timeout pour le mode privilégié *min* *sec*", "negate": True, "nohandler": exec_timeout},
            "no": {"description": "Inverser une commande", "negate": False, "nohandler": no},
            "exit": {"description": "Retourner au mode précédent", "negate": False, "handler": exit_mode},
            "end": {"description": "Retourner au mode privilégié", "negate": False, "handler": end}
        }
}

# ===================== ------------- =====================

hostname = 'Equipment'


nav = {
    "user": f"{hostname}> ",
    "privileged": f"{hostname}# ",
    "config": f"{hostname}(config)# ",
    "config if": f"{hostname}(config-if)# ",
    "config line": f"{hostname}(config-line)# "
    }

current_mode = {"mode": "user", "prompt": nav["user"]}


while True:
    user_input = input(current_mode["prompt"])
    
    handle_commands(user_input, current_mode, nav)
