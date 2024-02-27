import requests

"""
import re
with open("DynamicSystems2024-2/KantoPokemon.txt", "w+") as file:
    file.write("Pokemon de Kanto")
    link = "https://pokeapi.co/api/v2/pokemon/?limit=386"
    D = requests.get(link).json()
    for key in D["results"]:
        test = re.sub("/[0-9]*/$", "/" + key["name"] + "/", key["url"])
        file.write("\n" + test)

"""
"""
import re
file = open("KantoPokemon.txt", "r")
n = 132
link = file.readlines()[n][:-1]
poke = Pokemon(link)
poke.print()
file.close()
"""

"""
class Move:
    def __init__(self, link):
        data = requests.get(link).json()
        self.id = data["id"]
        self.accuracy = data["accuracy"]
        self.damage_class = data["damage_class"]['name']
        self.effect_chance = data["effect_chance"]
        self.name = data["name"]
        self.power = data["power"]
        self.pp = data['pp']
        self.priority = data["priority"]
        self.type = data["type"]["name"]
        if len(data["effect_entries"]):
            self.effect_entries = data["effect_entries"][0]["effect"].replace(
                "$effect_chance", str(self.effect_chance)
            )
        else:
            self.effect_entries = None
        if data['meta'] != None:
            self.ailment = data['meta']['ailment']['name']
        else: self.ailment = None

    def print(self):
        print("Id :", self.id)
        print("Name :", self.name.capitalize())
        print("Type :", self.type.capitalize())
        print("damage_class :", self.damage_class.capitalize())
        print("Power :", self.power)
        print("PP :", self.pp)
        print("Accuracy :", self.accuracy)
        print("Priority :", self.priority)
        print('Ailment :',self.ailment)
        print("Effect_chance :", self.effect_chance)
        print("effect_entries :", self.effect_entries)
"""
class Type:
    damage_relations = {}
    def __init__(self, link):
        data = requests.get(link).json()
        self.id = data["id"]
        self.name = data['name']
        for key in data["damage_relations"]:
            if len(data["damage_relations"][key]):
                L = []
                for t in data['damage_relations'][key][0]:
                    if t == "name": L.append(data["damage_relations"][key][0][t])
                self.damage_relations[key] = L
            else: self.damage_relations[key] = ''

    def print(self):
        print("Id :", self.id)
        print("Name :", self.name.capitalize())
        for key in self.damage_relations:
            print(f'{key}:')
            for t in self.damage_relations[key]:
                print(f'\t{t}')


# move = Move("https://pokeapi.co/api/v2/move/tera-blast/")  # fire_punch (7) tri-attack (161) swords-dance (14)
# move.print()

typ = Type("https://pokeapi.co/api/v2/type/1/")
typ.print()
"""
link = "https://pokeapi.co/api/v2/type/1/"
# link = "https://pokeapi.co/api/v2/evolution-chain/2"
respt = requests.get(link).json()
for subkey in respt["damage_relations"]:
    # if subkey != "pokemon" and subkey != "names" and subkey != "moves":
    print(subkey)
    print(respt["damage_relations"][subkey])
    print()
"""
