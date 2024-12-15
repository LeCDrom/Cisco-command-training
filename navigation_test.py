import random
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

expected_config = {
    "hostname": "Switch"
}

# =================================

global prompt
prompt = {
    "user": f"{running_config["hostname"]}> ",
    "privileged": f"{running_config["hostname"]}# ",
    "config": f"{running_config["hostname"]}(config)# ",
    "config if": f"{running_config["hostname"]}(config-if)# ",
    "config line": f"{running_config["hostname"]}(config-line)# "
}

def open_file(name: str) -> str:
    data = ""
    with open(name, 'r') as f:
        for line in f:
            data += line
    f.close()
    return data

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

def print_help(current: dict, modes: dict, usr_input: str, args: str):
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

# =================== Procedural task generation ===================

def random_hostname():
    """Génère un hostname aléatoire"""
    return f"{random.choice(["SW", "RT", "Info", "ICom"])}{random.randint(1, 30)}{random.choice(["-0etage", "-1etage", "-2etage"])}"

def random_interface():
    """Génère une interface aléatoire"""
    interface = random.choice(["FastEthernet", "GigabitEthernet", "vlan"])
    if interface == "FastEthernet":
        return f"{interface}0/{random.randint(1, 24)}"
    elif interface == "GigabitEthernet":
        return f"{interface}0/{random.randint(1, 2)}"
    else:
        return f"{interface} {random.choice([random.randint(1, 40), random.randint(1, 150)])}"

def random_ip():
    """Génère un adresse IP aléatoire"""
    return f"{random.choice([f"192.168.{random.randint(0, 254)}.{random.randint(0, 254)}", f"172.16.{random.randint(0, 254)}.{random.randint(1, 254)}", f"10.{random.randint(0, 254)}.{random.randint(0, 254)}.{random.randint(1, 254)}"])}"

def random_mask_cidr(ip):
    """Génère un masque aléatoire (notation CIDR)"""
    if ip.startswith("192.168") or ip.startswith("172.16"):
        return f"/{random.choice(["16", "24"])}"
    else:
        return f"/{random.choice(["8", "16", "24"])}"

def random_mask(ip):
    """Génère un masque aléatoire"""
    masks = {
        8: "255.0.0.0",
        16: "255.255.0.0",
        24: "255.255.255.0"
    }
    prefix = list(masks.keys())

    if ip.startswith("192.168") or ip.startswith("172.16"):
        return f"{masks[random.choice(prefix[1:])]}"
    else:
        return f"{masks[random.choice(prefix)]}"

def random_speed(duplex):
    """Génère une vitesse de transmission aléatoire"""
    if duplex == "half-duplex":
        return "10"
    else:
        return random.choice(["10", "100", "1000"])

def random_duplex():
    """Génère un mode de transmission aléatoire"""
    return random.choice(["auto", "full-duplex", "half-duplex"])

def random_description(interface):
    """Génère une description aléatoire"""
    if "vlan" in interface:
        return random.choice(["Services logiciels", "Comptabilité", "Administratif", "Vente", "Supervision", "Administration Informatique"])
    else:
        return f"{random.choice(["Cœur", "Distribution", "Accès"])}-{random.randint(1, 10)}"

def random_username():
    """Génère un nom d'utilisateur aléatoire"""
    return random.choice(["bob", "alice", "eddy-malou", "admin", "linus"])

def random_password():
    """Génère un mot de passe aléatoire"""
    return random.choice["pouzin", "cisco", "savant", "L3:MDp:h@rD:5", "swiche"]

def random_lines():
    """Génère des lignes aléatoires"""
    item = random.choice(["console", "vty"])
    if item == "console":
        return "console 0"
    else:
        line1 = random.randint(0, 3)
        line2 = random.randint(1, 6)
        while line2 < line1 and line2 != line1:
            line2 = random.randint(1, 6)
        return f"vty {line1} {line2}"

for _ in range(30):
    print(random_lines())

def new_task():
    pass

def check_results():
    pass

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


global commands_list
commands_list = {
        "user": {
            "enable": {"description": "Passer en mode privilégié ⤒", "negate": False, "handler": enable},
            "en": {"description": "Passer en mode privilégié ⤓", "negate": False, "handler": enable},
            "exit": {"description": "Retourner au mode précédent", "negate": False, "handler": exit_mode},
            "?": {"description": "Affiche les commandes disponibles dans le mode actuel", "negate": False, "handler": print_help},
            "::check": {"description": "Vérification des résultats", "negate": False, "handler": check_results},
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
            "?": {"description": "Affiche les commandes disponibles dans le mode actuel", "negate": False, "handler": print_help},
            "::check": {"description": "Vérification des résultats", "negate": False, "handler": check_results},
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
            "?": {"description": "Affiche les commandes disponibles dans le mode actuel", "negate": False, "handler": print_help},
            "::check": {"description": "Vérification des résultats", "negate": False, "handler": check_results},
        },

        "config if": {
            "duplex": {"description": "Définir le mode de transmission [ auto | half | full ]", "negate": False, "nohandler": duplex},
            "speed": {"description": "Définir la vitesse de transmission [ auto | 10 | 100 ]", "negate": False, "nohandler": speed},
            "description": {"description": "Établir la description de l'interface", "negate": True, "nohandler": descript},
            "shutdown": {"description": "Éteindre / désactiver l'interface", "negate": True, "nohandler": shutdown},
            "switchport": {"description": "Configurer le type de port", "negate": False, "nohandler": switchport},
            "no": {"description": "Inverser une commande", "negate": False, "handler": no},
            "exit": {"description": "Retourner au mode précédent", "negate": False, "handler": exit_mode},
            "end": {"description": "Retourner au mode privilégié", "negate": False, "handler": end},
            "?": {"description": "Affiche les commandes disponibles dans le mode actuel", "negate": False, "handler": print_help},
            "::check": {"description": "Vérification des résultats", "negate": False, "handler": check_results},
        },

        "config line": {
            "password": {"description": "Définir un mot de passe", "negate": True, "nohandler": password},
            "login": {"description": "Activer authentification", "negate": True, "nohandler": login},
            "transport": {"description": "Activer authentification", "negate": True, "nohandler": transport},
            "exec-timeout": {"description": "Définir un timeout pour le mode privilégié *min* *sec*", "negate": True, "nohandler": exec_timeout},
            "no": {"description": "Inverser une commande", "negate": False, "nohandler": no},
            "exit": {"description": "Retourner au mode précédent", "negate": False, "handler": exit_mode},
            "end": {"description": "Retourner au mode privilégié", "negate": False, "handler": end},
            "?": {"description": "Affiche les commandes disponibles dans le mode actuel", "negate": False, "handler": print_help},
            "::check": {"description": "Vérification des résultats", "negate": False, "handler": check_results},
        }
}


current_mode = {"mode": "user", "prompt": prompt["user"]}


while True:
    user_input = input(current_mode["prompt"])
    
    handle_commands(user_input, prompt, current_mode)
