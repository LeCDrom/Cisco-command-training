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
    "root": f"{hostname}# ",
    "term": f"{hostname}(config)# ",
    "line": f"{hostname}(config-if)# "
    }

while True:
    user_input = input(nav["line"])
    result = command.parseString(user_input)
    print("Commande analysée avec succès :", result)
