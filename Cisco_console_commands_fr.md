### Commandes basiques (navigation et autres) :

```text
• SW1> enable
• SW1# configure terminal
• SW1(config)# hostname *HostName*
• HostName(config)# line console 0
• HostName(config-line)# exit
• HostName(config)# interface *FastEthernet0/1*
• HostName(config-if)# end
• HostName#
```

### Configurer le nom de l'équipement :

```text
• HostName(config)# hostname *HostName*
```

### Sécuriser le mode utilisateur :

```text
• HostName(config)# line console 0
• HostName(config-line)# password *cisco*
• HostName(config-line)# login
```

### Sécuriser le mode privilégié :

```text
• HostName(config)# enable password *cisco* | ou
• HostName(config)# enable secret *cisco*   | => aucun effet si dans fichier config avec enable secret
• HostName(config)# no enable password
• HostName(config)# no enable secret
```

### Activer et sécuriser l'accès SSH à distance :

```text
• HostName(config)# line console 0
• HostName(config-line)# password *pouzin*
• HostName(config-line)# exit
• HostName(config)# ip domain name *site.com*
• HostName(config)# crypto key generate rsa modulus *2048*
• HostName(config)# username *Bob* secret *cisco*
• HostName(config)# line vty *0 4*
• HostName(config-line)# password *cisco*
• HostName(config-line)# login *local*
• HostName(config-line)# transport input [ ssh | telnet ]
```

### Afficher bannière :

```text
• HostName(config)# banner motd *#message#*
```

### Activer chiffrement des mots de passe :

```text
• HostName(config)# service password-encryption
```

### Sauvegarder la configuration :

```text
• HostName# copy running-config startup-config  | ou
• HostName# write                               |
```

### Restaurer la configuration :

```text
• HostName# copy startup-config running-config
```

### Supprimer la configuration :

```text
• HostName# erase startup-config    | ou
• HostName# write erase             |
• HostName# reload => redémarrer
```

### Configuration des interfaces :

```text
• HostName(config)# interface *type-and-number*
• HostName(config)# interface range *Fe0/1-4* => de port 1 à 4
• HostName(config-if)# description *description-text*
• HostName(config-if)# duplex [ auto | half | full ]
• HostName(config-if)# speed [ auto | 10 | 100 ]
• HostName(config-if)# ip address *ipv4-address* *masque*
• HostName(config-if)# ipv6 address *ipv6-address*/*longueur-préfixe*
• HostName(config-if)# no shutdown
```

### Créer / supprimer Vlan :

```text
• HostName(config)# erase vlan.dat [EFFACER TOUTES LES VLAN]
• HostName(config)# vlan *10*
• HostName(config-vlan)# exit
• HostName(config)# interface vlan *10*
• HostName(config-if)# ip address *ipv4-address* *masque*
• HostName(config-if)# exit
• HostName(config)# exit
• HostName# show vlan
• HostName# no vlan *10*
```

### Attribuer port d'accès au Vlan :

```text
• HostName(config)# interface *FastEthernet0/1*
• HostName(config-if)# switchport mode access [OPTIONNEL]
• HostName(config-if)# switchport access vlan *10*
• HostName(config-if)# no shutdown
```

### Attribuer port taggué au Vlan :

```text
• HostName(config)# interface FastEthernet0/1
• HostName(config-if)# switchport trunk allowed vlan *10* add
• HostName(config-if)# no shutdown
```

### Sécuriser le réseau :

```text
• HostName# auto secure
• HostName(config)# service password-encryption
• HostName(config)# security password min-length *8*
• HostName(config)# login block-for *120* attempts *3* within *60*  
  => bloque pendant 120s si 3 essais échoués en l'espace de 60s
• HostName(config-line)# exec-timeout *5* *30* => 5min 30s
```

### Activer / désactiver Spanning-Tree (STP) :

```text
• HostName# spanning-tree => activer
• HostName# spanning-tree mode [ stp | rstp | mst ]
• HostName# show spanning-tree
• HostName# no spanning-tree => désactiver
```

### Trucs à savoir

```text
- Taper "?" pour obtenir une liste des commandes possibles
- Ajouter mot de passe console avant de configurer SSH*
- Généralement préfixe "no" pour inverser la commande (no shutdown)
- Commande "ping" ou "traceroute" seule pour entrer dans commande détaillée
- Port Fa : Fast Ethernet ; Port Gi : Gigabit Ethernet
```

### Commandes en vrac :

```text
• HostName# show running-config
• HostName# show startup-config
• HostName# show ip interface brief => afficher toutes les interfaces (+ Vlan)
• HostName# show ip route
• HostName# show interfaces [SUPER LONG]
• HostName# show interface *Fa0/1*
• HostName# show ip interface
• HostName# show mac address-table
• HostName# show vlan
• HostName# show version
• HostName# show arp
• HostName# show protocols
• HostName# show interfaces switchport => afficher ports actifs
• HostName# show ip ports all
• HostName# show users => afficher sessions SSH / Telnet actives
• HostName# show running-config | include username => afficher utilisateurs créés sur l'équipement

• Router# show ip route
• Router# show cdp neighbors => afficher voisins (Cisco Discovery Protocol)
• Router# no cdp enable

• HostName# debug ip icmp => activer verbose pour commande ping (debug)
• HostName# undebug all => désactiver verbose pour toutes les commandes (debug)
• HostName# terminal monitor => enable terminal verbose

• HostName# write => sauvegarder config
• HostName# write erase => supprimer config

• HostName(config-if)# no description => supprimer description
• HostName# no ip *service* => désactiver protocole (http server, http secure-server...)
• HostName# no username *bob* => supprimer un utilisateur


• HostName# ping *destination*
• HostName# traceroute *destination*
```
