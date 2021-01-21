#GNS3_Autoscript
import json
import string
import random
import os
import ipaddress

with open('config.json') as json_file:
    data = json.load(json_file)
    project_name = data["project_name"]

#listes importantes
data_routers_dict = {}
data_routers_dict.update(data["P"])
data_routers_dict.update(data["PE"])
data_routers_dict.update(data["CE"])

routersP_names = list(data["P"].keys())
routersPE_names = list(data["PE"].keys())
routersCE_names = list(data["CE"].keys())
PCs = data["PC"]
wires = list(data["links"].keys())
flux_vpn = list(data["Protocols"]["VPN"].keys())
backbone_nodes = routersP_names + routersPE_names
routers_names = backbone_nodes + routersCE_names

# genreation du project_id
part1 = string.ascii_uppercase[0:6]
part2 = string.ascii_lowercase[0:6]
part3 = string.digits
project_id = "".join(random.choice(part1+part2+part3) for i in range(8)) + "-" + "".join(random.choice(part1+part2+part3) for i in range(4)) + "-" + "".join(random.choice(part1+part2+part3) for i in range(4)) + "-" + "".join(random.choice(part1+part2+part3) for i in range(4)) + "-" + "".join(random.choice(part1+part2+part3) for i in range(12))

# dictionnaire qui associe un flux à ses CE
#clef = nom_flux (la dernière c'est new)
#valeur = liste de routeurs
routers_CE_names_copy = routersCE_names.copy()
flux_vpn_CE = {}
for vpn_name in flux_vpn:
    routers_CE_flux_names = data["Protocols"]["VPN"][vpn_name].split("/")
    flux_vpn_CE[vpn_name] = routers_CE_flux_names
    for router in routers_CE_flux_names:
        routers_CE_names_copy.remove(router)
# on met tous les autres CE dans un flux vpn "NEW" ouvert
flux_vpn_CE["NEW"] = routers_CE_names_copy

# instanciation de la liste des routeurs
router_dict = {}
for index, router_name in enumerate(routers_names):
    router_dict[router_name] = {
        # identifiants
        "id" : "".join(random.choice(part1+part2+part3) for i in range(8)) + "-" + "".join(random.choice(part1+part2+part3) for i in range(4)) + "-" + "".join(random.choice(part1+part2+part3) for i in range(4)) + "-" + "".join(random.choice(part1+part2+part3) for i in range(4)) + "-" + "".join(random.choice(part1+part2+part3) for i in range(12)),
        "dynamips_id" : index+1,
        # infos utiles
        "name" : router_name,
        "loopback_address" : data_routers_dict[router_name],
        "PE" : router_name in routersPE_names,
        "CE" : router_name in routersCE_names,
        "P" : router_name in routersP_names,
        "slots" : [ # le slot f0/0 est reservé pour les PCs
            "g1/0",
            "g2/0",
            "g3/0",
            "g4/0"
        ],
        "interfaces" : {}
        #     # boucle for pour les slots
        #     interface_name : {
        #         "interface_addr" : "",
        #         "net_addr" : "",
        #         "mask_addr" : "",
        #         "inversed_mask" : "",
        #         "neighbor" : {
        #               "slot_voisin" : "",
        #               "router_voisin" : ""
        #         }
        #     },
        #}
    }

# instanciation de la liste de PCs
pc_dict = {}
for pc_name in PCs:
    pc_dict[pc_name] = {
        "id" : "".join(random.choice(part1+part2+part3) for i in range(8)) + "-" + "".join(random.choice(part1+part2+part3) for i in range(4)) + "-" + "".join(random.choice(part1+part2+part3) for i in range(4)) + "-" + "".join(random.choice(part1+part2+part3) for i in range(4)) + "-" + "".join(random.choice(part1+part2+part3) for i in range(12)),
        "interfaces" : {}
        #"interface_addr" : "",
        #"mask_addr" : "",
        #"neighbor" : {
        #    "slot_voisin" : "",
        #    "router_voisin" : ""
        #}
    }

mac_adresses = [
    "ca08.526a.0000",
    "ca07.376d.0000",
    "ca07.5251.0000",
    "ca06.375e.0000",
    "ca06.523f.0000",
    "ca05.374f.0000",
    "ca05.522a.0000",
    "ca04.3740.0000",
    "ca04.7a5f.0000",
    "ca03.36c4.0000",
    "ca03.7a4f.0000",
    "ca02.36b5.0000",
    "ca02.7a3f.0000",
    "ca01.366c.0000",
    "ca01.7a2f.0000"
]
"""
#option of configuration:
    -Avec mpls et ospf
    -avec VPN
    -All the nodes will be under the same ospf and area, eeveryone is backbone except PCs

#order
    -project name
    -instanciate each node like:
        R1 : 1.1.1.1(loopback and router id)
        PC1 : 192.168.1.1/8 (pc ip @)
    -write down each connection like
        R1/R2 : 192.168.10.0/24

"""


config_file = {}
config_file = {
    "auto_close": True,
    "auto_open": False,
    "auto_start": False,
    "drawing_grid_size": 25,
    "grid_size": 75,
    "name": project_name,
    "project_id": project_id,
    "revision": 9,
    "scene_height": 1000,
    "scene_width": 2000,
    "show_grid": False,
    "show_interface_labels": False,
    "show_layers": False,
    "snap_to_grid": False,
    "supplier": None,
    "topology": {
        "computes" : []
    }
}

# on garde un dessin sinon il va pas aimer
drawings = []
drawing_id = "".join(random.choice(part1+part2+part3) for i in range(8)) + "-" + "".join(random.choice(part1+part2+part3) for i in range(4)) + "-" + "".join(random.choice(part1+part2+part3) for i in range(4)) + "-" + "".join(random.choice(part1+part2+part3) for i in range(4)) + "-" + "".join(random.choice(part1+part2+part3) for i in range(12))

drawings = [
    {
        "drawing_id": drawing_id,
        "locked": False,
        "rotation": 0,
        "svg": "<svg height=\"32\" width=\"211\"><text fill=\"#000000\" fill-opacity=\"1.0\" font-family=\"TypeWriter\" font-size=\"10.0\" font-weight=\"bold\">XXXXXXX /32</text></svg>",
        "x": 0,
        "y": 0,
        "z": 2
    },{}
]
config_file["topology"]["drawings"] = drawings


# on ajoute les routeurs au tableau nodes pour le config_file de GNS3
base = -600
console = 4999
nodes = []
for router in router_dict:
    #varialbes
    base = base + 100
    console = console + 1

    #JSON
    temp = {
        "compute_id": "local",
        "console": console,
        "console_auto_start": False,
        "console_type": "telnet",
        "custom_adapters": [],
        "first_port_name": None,
        "height": 45,
        "label": {
            "rotation": 0,
            "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
            "text": router,
            "x": 14,
            "y": 14
        },
        "locked": False,
        "name": router,
        "node_id": router_dict[router]["id"],
        "node_type": "dynamips",
        "port_name_format": "Ethernet{0}",
        "port_segment_size": 0,
        "properties": {
            "auto_delete_disks": True,
            "aux": None,
            "clock_divisor": 4,
            "disk0": 0,
            "disk1": 0,
            "dynamips_id": router_dict[router]["dynamips_id"],
            "exec_area": 64,
            "idlemax": 500,
            "idlepc": "0x62cc930c",
            "idlesleep": 30,
            "image": "c7200-advipservicesk9-mz.152-4.S5.image",
            "image_md5sum": "cbbbea66a253f1dac0fcf81274dc778d",
            "mac_addr": mac_adresses.pop(),
            "midplane": "vxr",
            "mmap": True,
            "npe": "npe-400",
            "nvram": 512,
            "platform": "c7200",
            "power_supplies": [
                1,
                1
            ],
            "ram": 512,
            "sensors": [
                22,
                22,
                22,
                22
            ],
            "slot0": "C7200-IO-FE",
            "slot1": "PA-GE",
            "slot2": "PA-GE",
            "slot3": "PA-GE",
            "slot4": "PA-GE",
            "slot5": None,
            "slot6": None,
            "sparsemem": True,
            "system_id": "FTX0945W0MY",
            "usage": ""
        },
        "symbol": ":/symbols/router.svg",
        "template_id": "0ecbc8b2-7491-47f1-9e02-b331eafea650",
        "width": 66,
        "x": base,
        "y": base,
        "z": 1
    }
    nodes.append(temp)

# on ajoute les PCs au tableau nodes pour le config_file de GNS3
x1 = 650
y1 = -550
for pc in PCs:
    x1 = x1 - 100
    y1 = y1 + 100
    #varialbes
    console = console + 1

    temp = {
        "compute_id": "local",
        "console": console,
        "console_auto_start": False,
        "console_type": "telnet",
        "custom_adapters": [],
        "first_port_name": None,
        "height": 59,
        "label": {
            "rotation": 0,
            "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
            "text": pc,
            "x": 0,
            "y": 0
        },
        "locked": False,
        "name": pc,
        "node_id": pc_dict[pc]["id"],
        "node_type": "vpcs",
        "port_name_format": "Ethernet{0}",
        "port_segment_size": 0,
        "properties": {},
        "symbol": ":/symbols/vpcs_guest.svg",
        "template_id": "19021f99-e36f-394d-b4a1-8aaa902ab9cc",
        "width": 65,
        "x": x1,
        "y": y1,
        "z": 1
    }
    nodes.append(temp)

# on ajoute le tableau nodes (routeurs + PCs) au config_file pour GNS3
config_file["topology"]["nodes"] = nodes

#ECRIRE PC EN PERMIER : PC1/R1
links = []
nodes_dict = {}
nodes_dict.update(router_dict)
nodes_dict.update(pc_dict)
for wire in wires:
    #variables
    link_id = "".join(random.choice(part1+part2+part3) for i in range(8)) + "-" + "".join(random.choice(part1+part2+part3) for i in range(4)) + "-" + "".join(random.choice(part1+part2+part3) for i in range(4)) + "-" + "".join(random.choice(part1+part2+part3) for i in range(4)) + "-" + "".join(random.choice(part1+part2+part3) for i in range(12))
    interface1 = ""
    interface2 = ""


    IPv4_adress = ipaddress.IPv4Network(data["links"][wire])
    net_address = str(IPv4_adress.network_address)
    net_mask = str(IPv4_adress.netmask)
    net_host_list = list(IPv4_adress.hosts())
    inversed_masked = str(IPv4_adress.hostmask)
    extremities = wire.split("/")
    extr1 = extremities[0]
    extr2 = extremities[1]

    #si l'interface 1 et 2 sont des routeur on les donnent un slot a partir de router_dict
    #QUE LA PREMIERE INTERFACE PEUT ETRE PC???????
    if (extr1 in routers_names) and (extr2 in routers_names):
        interface1 = router_dict[extr1]["slots"].pop()
        interface2 = router_dict[extr2]["slots"].pop()
        # associe slot : slotvoisin/routeurvoisin
        #interfaces :
        router_dict[extr1]["interfaces"][interface1] = {
            "interface_addr" : str(net_host_list.pop(0)),
            "net_addr" : net_address,
            "mask_addr" : net_mask,
            "inversed_mask" : inversed_masked,
            "neighbors" : {
                "slot_voisin" : interface2,
                "router_voisin" : extr2
            }
        }
        router_dict[extr2]["interfaces"][interface2] = {
            "interface_addr" : str(net_host_list.pop(0)),
            "net_addr" : net_address,
            "mask_addr" : net_mask,
            "inversed_mask" : inversed_masked,
            "neighbors" : {
                "slot_voisin" : interface1,
                "router_voisin" : extr1
            }
        }

    # si extr1 est un PC :
    if extr1 in PCs:
        interface1 = "e0"
        interface2 = "f0/0"

        pc_dict[extr1]["interfaces"] = {
            "interface_addr" : str(net_host_list.pop(0)),
            "mask_addr" : net_mask,
            "neighbor" : {
                "slot_voisin" : interface2,
                "router_voisin" : extr2
            }
        }
        router_dict[extr2]["interfaces"][interface2] = {
            "interface_addr" : str(net_host_list.pop(0)),
            "net_addr" : net_address,
            "mask_addr" : net_mask,
            "inversed_mask" : inversed_masked,
            "neighbor" : {
                "slot_voisin" : interface1,
                "router_voisin" : extr1
            }
        }

    temp = {
        "filters": {},
        "link_id": link_id,
        "nodes": [
            {
                "adapter_number": int(interface1[1]), # on prend le deuxième caractère
                "label": {
                    "rotation": 0,
                    "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
                    "text": interface1,
                    "x": int(interface1[1]),
                    "y": int(interface1[1])
                },
                "node_id": nodes_dict[extr1]["id"],
                "port_number": 0
            },
            {
                "adapter_number": int(interface2[1]),
                "label": {
                    "rotation": 0,
                    "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
                    "text": interface2,
                    "x": int(interface2[1]),
                    "y": int(interface2[1])
                },
                "node_id": nodes_dict[extr2]["id"],
                "port_number": 0
            }
        ],
        "suspend": False
    }
    links.append(temp)

# on ajoute les liens au config_file pour GNS3
config_file["topology"]["links"] = links






rest = {}
rest = {
    "type": "topology",
    "variables": None,
    "version": "2.2.16",
    "zoom": 50
}

config_file.update(rest)

#print(json.dumps(config_file, indent=4))

with open(project_name+'.gns3','w') as f:
    f.write(json.dumps(config_file, indent=4))



#---------------------------------------------------------------------------------------------------------------
#                                               Each router configuration
#---------------------------------------------------------------------------------------------------------------
current_path = os.getcwd()

# routeurs de coeur
for router in routersP_names:
    router_config = """!
!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
!
hostname """+router+"""
!
boot-start-marker
boot-end-marker
!
!
!
no aaa new-model
no ip icmp rate-limit unreachable
ip cef
!
!
!
!
!
!
no ip domain lookup
no ipv6 cef
!
!
mpls label range """+str((router_dict[router]["dynamips_id"])*100)+""" """+str(((router_dict[router]["dynamips_id"])*100)+99)+"""
multilink bundle-name authenticated
!
!
!
!
!
!
!
!
!
ip tcp synwait-time 5
!
!
!
!
!
!
!
!
!
!
!
!
interface Loopback1
 ip address """ + router_dict[router]["loopback_address"] + """ 255.255.255.255
!
interface FastEthernet0/0
 no ip address
 shutdown
 duplex full
!
"""
    for i in range(1,5):
        interf = "g"+str(i)+"/0"
        router_config += "interface GigabitEthernet"+str(i)+"/0\n"
        if interf in router_dict[router]["slots"]:
            #pas d'@
            router_config += " no ip address\n"
            router_config += " shutdown\n"
            router_config += " negotiation auto \n!\n"
        else:
            router_config += " ip address "+router_dict[router]["interfaces"][interf]["interface_addr"]+" "+router_dict[router]["interfaces"][interf]["mask_addr"]+"\n"
            router_config += " negotiation auto\n"
            router_config += " mpls ip\n"
            router_config += " mpls mtu "+str(data["Protocols"]["MPLS"])+"\n"
            router_config += " no keepalive \n!\n"

    router_config += "router ospf 1\n"
    router_config += " router-id " + router_dict[router]["loopback_address"] + "\n"
    router_config += " network " + router_dict[router]["loopback_address"] + " 0.0.0.0 area 0\n"
    list_interfaces = list(router_dict[router]["interfaces"].keys())
    for interface in list_interfaces:
        router_config += " network " + router_dict[router]["interfaces"][interface]["net_addr"] + " " + router_dict[router]["interfaces"][interface]["inversed_mask"] + " area 0\n"

    router_config += """!
ip forward-protocol nd
!
!
no ip http server
no ip http secure-server
!
!
mpls ldp router-id Loopback1
!
!
control-plane
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line vty 0 4
 login
!
!
end"""

    path = current_path+"/project-files/dynamips/"+router_dict[router]["id"]+"/configs"
    try:
        os.makedirs(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s" % path)
    with open('project-files/dynamips/'+router_dict[router]["id"]+'/configs/i'+str(router_dict[router]["dynamips_id"])+'_startup-config.cfg','w') as f:
        f.write(router_config)

# routeurs CE
for router in routersCE_names:
    router_config = """!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
!
hostname """+router+"""
!
boot-start-marker
boot-end-marker
!
!
!
no aaa new-model
no ip icmp rate-limit unreachable
ip cef
!
!
!
!
!
!
no ip domain lookup
no ipv6 cef
!
!
multilink bundle-name authenticated
!
!
!
!
!
!
!
!
!
ip tcp synwait-time 5
!
!
!
!
!
!
!
!
!
!
!
!
interface Loopback1
 ip address """ + router_dict[router]["loopback_address"] + """ 255.255.255.255
!
"""
    #il a un ordi ou pas?
    if "f0/0" in router_dict[router]["slots"]:
        router_config += """interface FastEthernet0/0
 no ip address
 shutdown
 duplex full
!
"""
    else:
        router_config += "interface FastEthernet0/0\n"
        router_config += " ip address "+router_dict[router]["interfaces"]["f0/0"]["interface_addr"]+" "+router_dict[router]["interfaces"]["f0/0"]["mask_addr"]+"\n"
        router_config += " ip ospf 1 area 0\n"
        router_config += " duplex full\n"
        router_config += " no keepalive \n!\n"

    for i in range(1,5):
        interf = "g"+str(i)+"/0"
        router_config += "interface GigabitEthernet"+str(i)+"/0\n"
        if interf in router_dict[router]["slots"]:
            #pas d'@
            router_config += " no ip address\n"
            router_config += " shutdown\n"
            router_config += " negotiation auto\n!\n"
        else:
            router_config += " ip address "+router_dict[router]["interfaces"][interf]["interface_addr"]+" "+router_dict[router]["interfaces"][interf]["mask_addr"]+"\n"
            router_config += " ip ospf 1 area 0\n"
            router_config += " negotiation auto\n"
            router_config += " no keepalive \n!\n"

    router_config += "router ospf 1\n"
    router_config += " router-id " + router_dict[router]["loopback_address"] + "\n"
    list_interfaces = list(router_dict[router]["interfaces"].keys())
    for interface in list_interfaces:
        router_config += " network " + router_dict[router]["interfaces"][interface]["net_addr"] + " " + router_dict[router]["interfaces"][interface]["inversed_mask"] + " area 0\n"
    router_config += """!
ip forward-protocol nd
!
!
no ip http server
no ip http secure-server
!
!
!
!
control-plane
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line vty 0 4
 login
!
!
end"""
    path = current_path+"/project-files/dynamips/"+router_dict[router]["id"]+"/configs"
    try:
        os.makedirs(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s" % path)
    with open('project-files/dynamips/'+router_dict[router]["id"]+'/configs/i'+str(router_dict[router]["dynamips_id"])+'_startup-config.cfg','w') as f:
        f.write(router_config)

# routeurs PE
for router in routersPE_names:
    router_config ="""!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
!
hostname """+router+"""
!
boot-start-marker
boot-end-marker
!
!
!
no aaa new-model
no ip icmp rate-limit unreachable
ip cef
!
ip vrf NEW
 rd 25253:8000
 route-target export 25253:8000
 route-target import 25253:8000
 route-target import 25253:9000
!
"""
    counter = 100
    for flux in flux_vpn:
        router_config += "ip vrf " + flux + "\n"
        router_config += " rd 25253:"+str(counter)+"\n"
        router_config += " route-target export 25253:"+str(counter)+"\n"
        router_config += " route-target import 25253:"+str(counter)+"\n"
        router_config += " route-target import 25253:8000\n"
        router_config += " route-target export 25253:9000\n!\n"
        counter += 100

    router_config +="""!
!
!
!
!
no ip domain lookup
no ipv6 cef
!
!
mpls label range """+str((router_dict[router]["dynamips_id"])*100)+""" """+str(((router_dict[router]["dynamips_id"])*100)+99)+"""
multilink bundle-name authenticated
!
!
!
!
!
!
!
!
!
ip tcp synwait-time 5
!
!
!
!
!
!
!
!
!
!
!
!
interface Loopback1
 ip address """ + router_dict[router]["loopback_address"] + """ 255.255.255.255
!
interface FastEthernet0/0
 no ip address
 shutdown
 duplex full
!
"""
    # gestion des interfaces
    for i in range(1,5):
        interf = "g"+str(i)+"/0"
        router_config += "interface GigabitEthernet"+str(i)+"/0\n"
        if interf not in router_dict[router]["slots"]: # c'est connecté
            neighbor = router_dict[router]["interfaces"][interf]["neighbors"]["router_voisin"]
            if neighbor in backbone_nodes:
                router_config += " ip address "+router_dict[router]["interfaces"][interf]["interface_addr"]+" "+router_dict[router]["interfaces"][interf]["mask_addr"]+"\n"
                #router_config += " ip ospf 1 area 0\n" #ENLEVER DES AUTRES!!!
                router_config += " negotiation auto\n"
                router_config += " mpls ip\n"
                router_config += " mpls mtu "+str(data["Protocols"]["MPLS"])+"\n!\n"
            elif neighbor in routersCE_names:
                for vpn_name in list(flux_vpn_CE.keys()):
                    if neighbor in flux_vpn_CE[vpn_name]:
                        router_config += " ip vrf forwarding "+vpn_name+"\n"
                        router_config += " ip address "+router_dict[router]["interfaces"][interf]["interface_addr"]+" "+router_dict[router]["interfaces"][interf]["mask_addr"]+"\n"
                        router_config += " negotiation auto \n!\n"
        else: # c'est pas connecté
            router_config += " no ip address\n"
            router_config += " shutdown\n"
            router_config += " negotiation auto \n!\n"

    # OSPF avec backbone
    router_config += "router ospf 1\n"
    list_interfaces = list(router_dict[router]["interfaces"].keys())
    for interface in list_interfaces:
        neighbor = router_dict[router]["interfaces"][interface]["neighbors"]["router_voisin"]
        if neighbor in backbone_nodes:
            router_config += " network " + router_dict[router]["interfaces"][interface]["net_addr"] + " " + router_dict[router]["interfaces"][interface]["inversed_mask"] + " area 0\n"
    router_config += " network "+ router_dict[router]["loopback_address"] + " 0.0.0.0 area 0\n!\n"

    # les autres OSPF
    for index, vpn_name in enumerate(list(flux_vpn_CE.keys())):
        router_config += "router ospf " + str(index + 2) + " vrf "+vpn_name+"\n"
        router_config += " redistribute bgp 25253 subnets\n"
        for interface in list_interfaces:
            neighbor = router_dict[router]["interfaces"][interface]["neighbors"]["router_voisin"]
            if neighbor in flux_vpn_CE[vpn_name]:
                router_config += " network " + router_dict[router]["interfaces"][interface]["net_addr"] + " " + router_dict[router]["interfaces"][interface]["inversed_mask"] + " area 0\n!\n"

    #le bgp #PB : faire avec tout les routerus PE
    router_config += "router bgp 25253\n"
    router_config += " bgp log-neighbor-changes\n"
    for bgp_neighbor in routersPE_names:
        if bgp_neighbor != router:
            router_config +=  " neighbor "+router_dict[bgp_neighbor]["loopback_address"]+" remote-as 25253\n"
            router_config +=  " neighbor "+router_dict[bgp_neighbor]["loopback_address"]+" update-source Loopback1\n"
    router_config += " !\n"
    #for interface in list_interfaces:
        #neighbor = router_dict[router]["interfaces"][interface]["neighbors"]["router_voisin"]
        #if neighbor in routersPE_names:
            #router_config +=  " neighbor "+router_dict[neighbor]["loopback_address"]+" remote-as 25253\n"
            #router_config +=  " neighbor "+router_dict[neighbor]["loopback_address"]+" update-source Loopback1\n!\n"

    #address family VPN
    router_config += " address-family vpnv4\n"
    #for interface in list_interfaces:
        #neighbor = router_dict[router]["interfaces"][interface]["neighbors"]["router_voisin"]
        #if neighbor in routersPE_names:
    for bgp_neighbor in routersPE_names:
        if bgp_neighbor != router:
            router_config += "  neighbor "+router_dict[bgp_neighbor]["loopback_address"]+" activate\n"
            router_config += "  neighbor "+router_dict[bgp_neighbor]["loopback_address"]+" send-community extended\n"
            router_config += "  neighbor "+router_dict[bgp_neighbor]["loopback_address"]+" next-hop-self\n"
    router_config += " exit-address-family\n"

    #address family VRF
    for index, vpn_name in enumerate(list(flux_vpn_CE.keys())):
        router_config += " !\n address-family ipv4 vrf " + vpn_name + "\n"
        router_config += "  redistribute ospf "+str(index+2)+"\n"
        router_config += " exit-address-family\n"

    router_config += """!
ip forward-protocol nd
!
!
no ip http server
no ip http secure-server
!
!
mpls ldp router-id Loopback1
!
!
control-plane
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line vty 0 4
 login
!
!
end"""
    path = current_path+"/project-files/dynamips/"+router_dict[router]["id"]+"/configs"
    try:
        os.makedirs(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s" % path)
    with open('project-files/dynamips/'+router_dict[router]["id"]+'/configs/i'+str(router_dict[router]["dynamips_id"])+'_startup-config.cfg','w') as f:
        f.write(router_config)

for pc in PCs:
    pc_config ="""# This the configuration for """+pc+"""
#
# Uncomment the following line to enable DHCP
# dhcp
# or the line below to manually setup an IP address and subnet mask
ip """+pc_dict[pc]["interfaces"]["interface_addr"]+' '+pc_dict[pc]["interfaces"]["mask_addr"]+""" gateway """+router_dict[pc_dict[pc]["interfaces"]["neighbor"]["router_voisin"]]["interfaces"][pc_dict[pc]["interfaces"]["neighbor"]["slot_voisin"]]["interface_addr"]+"""
#
#
set pcname """+pc

    current_path = os.getcwd()
    path = current_path+"/project-files/vpcs/"+pc_dict[pc]["id"]
    try:
        os.makedirs(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s" % path)
    with open('project-files/vpcs/'+pc_dict[pc]["id"]+'/startup.vpc','w') as f:
        f.write(pc_config)
#PB : not ospf in interface, ospf loopback
#loopback 1 or 0?
