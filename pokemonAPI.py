import requests
import time

class Pokemon:
    stats = {
        "hp": 0,
        "attack": 0,
        "defense": 0,
        "special-attack": 0,
        "special-defense": 0,
        "speed": 0,
    }
    types = list()
    moves = list()
    abilities = list()

    def __init__(self, link: str):
        data = requests.get(link).json()
        self.id = data["id"]
        self.name = data["name"]
        self.weight = data["weight"]
        self.height = data["height"]
        for stat in data["stats"]:
            name = stat["stat"]["name"]
            self.stats[name] = stat["base_stat"]
        for type in data["types"]:
            self.types.append(type["type"]["name"])
        for move in data["moves"]:
            self.moves.append(move["move"]["name"])
        for ability in data["abilities"]:
            self.abilities.append(ability["ability"]["name"])

    def print(self):
        print(f"Id     : {self.id}")
        print(f"Name   : {(self.name).capitalize()}")
        print(f"Weight : {self.weight}")
        print(f"Height : {self.height}")
        print("Types   :")
        for type in self.types:
            print(f"\t{type.capitalize()}")
        print("Stats   :")
        for stat in self.stats:
            print("\t" + stat.capitalize(), ":", self.stats[stat])
        print("Moves   :")
        for move in self.moves:
            print(f"\t{move.capitalize()}")
        print("Abilities:")
        for ability in self.abilities:
            print(f"\t{ability.capitalize()}")

class Move:
    def __init__(self, link):
        data = requests.get(link).json()
        self.id = data["id"]
        self.accuracy = data["accuracy"]
        self.damage_class = data["damage_class"]["name"]
        self.effect_chance = data["effect_chance"]
        self.name = data["name"]
        self.power = data["power"]
        self.pp = data["pp"]
        self.priority = data["priority"]
        self.type = data["type"]["name"]
        if len(data["effect_entries"]):
            self.effect_entries = data["effect_entries"][0]["effect"].replace(
                "$effect_chance", str(self.effect_chance)
            )
        else:
            self.effect_entries = None
        if data["meta"] != None:
            self.ailment = data["meta"]["ailment"]["name"]
        else:
            self.ailment = None

    def print(self):
        print("Id :", self.id)
        print("Name :", self.name.capitalize())
        print("Type :", self.type.capitalize())
        print("damage_class :", self.damage_class.capitalize())
        print("Power :", self.power)
        print("PP :", self.pp)
        print("Accuracy :", self.accuracy)
        print("Priority :", self.priority)
        print("Ailment :", self.ailment)
        print("Effect_chance :", self.effect_chance)
        print("effect_entries :", self.effect_entries)

class Ability:
    def __init__(self, link):
        data = requests.get(link).json()
        self.id = data["id"]
        self.name = data["name"]
        for key in data["effect_entries"]:
            if key["language"]["name"] == "en":
                self.effect_entries = key["effect"].replace("\n", " ")

    def print(self):
        print(f"Id            : {self.id}")
        print(f"Name          : {self.name}")
        print(f"Effect_entries: {self.effect_entries}")

class Type:
    damage_relations = {}

    def __init__(self, link):
        data = requests.get(link).json()
        self.id = data["id"]
        self.name = data["name"]
        for key in data["damage_relations"]:
            if len(data["damage_relations"][key]):
                L = []
                for t in data["damage_relations"][key][0]:
                    if t == "name":
                        L.append(data["damage_relations"][key][0][t])
                self.damage_relations[key] = L
            else:
                self.damage_relations[key] = ""

    def print(self):
        print("Id :", self.id)
        print("Name :", self.name.capitalize())
        for key in self.damage_relations:
            print(f"{key}:")
            for t in self.damage_relations[key]:
                print(f"\t{t}")


pokemonD = {}
moveD = {}
abilityD = {}
typeD = {}


start = time.time()
with open("DynamicSystems2024-2/KantoPokemon.txt", "r") as file:
    for link in file.readlines()[1:10]:
        poke = Pokemon(link[:-1])
        print(poke.name)
        pokemonD[poke.name] = poke
        for t in poke.types:
            if t not in typeD:
                print(f'\t\t\t{t}')
                typ = Type(f"https://pokeapi.co/api/v2/type/{t}/")
                typeD[t] = typ
        for a in poke.abilities:
            if a not in abilityD:
                print("\t" + a)
                ability = Ability(f"https://pokeapi.co/api/v2/ability/{a}/")
                abilityD[a] = ability 
        for m in poke.moves:
            if m not in moveD:
                print("\t\t" + m)
                mov = Move(f"https://pokeapi.co/api/v2/move/{m}/")
                moveD[m] = mov
end = time.time()
print(end-start)
