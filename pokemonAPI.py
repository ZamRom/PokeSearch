import requests
import MySQLdb
import time

class Pokemon:
    def __init__(self, link: str):
        self.stats = {
            "hp": 0,
            "attack": 0,
            "defense": 0,
            "special-attack": 0,
            "special-defense": 0,
            "speed": 0,
        }
        self.types = list()
        self.moves = list()
        self.abilities = list()
        data = requests.get(link).json()
        self.id = data["id"]
        self.name = data["name"]
        self.weight = data["weight"]
        self.height = data["height"]
        for stat in data["stats"]:
            name = stat["stat"]["name"]
            self.stats[name] = stat["base_stat"]
        for tipe in data["types"]:
            self.types.append(tipe["type"]["name"])
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
        for tipe in self.types:
            print(f"\t{tipe.capitalize()}")
        print("Stats   :")
        for stat in self.stats:
            print("\t" + stat.capitalize(), ":", self.stats[stat])
        print("Moves   :")
        for move in self.moves:
            print(f"\t{move.capitalize()}")
        print("Abilities:")
        for ability in self.abilities:
            print(f"\t{ability.capitalize()}")

class Type:
    def __init__(self, link):
        data = requests.get(link).json()
        self.id = data["id"]
        self.name = data["name"]
        self.damage_relations = {}
        for key in data["damage_relations"]:
            if len(data["damage_relations"][key]):
                L = []
                for t in data["damage_relations"][key]:
                    L.append(t["name"])
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
        self.tipe = data["type"]["name"]
        if len(data["effect_entries"]):
            self.effect_entries = data["effect_entries"][0]["effect"].replace(
                "$effect_chance", str(self.effect_chance)
            )
            self.effect_entries = self.effect_entries.replace("\n", " ")
        else:
            self.effect_entries = None
        if data["meta"] != None:
            self.ailment = data["meta"]["ailment"]["name"]
        else:
            self.ailment = None

    def print(self):
        print("Id :", self.id)
        print("Name :", self.name.capitalize())
        print("Type :", self.tipe.capitalize())
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
        try:
            len(self.effect_entries)
        except AttributeError:
            self.effect_entries = ""

    def print(self):
        print(f"Id            : {self.id}")
        print(f"Name          : {self.name}")
        print(f"Effect_entries: {self.effect_entries}")


def evoChain(link):
    data = requests.get(link).json()
    if len(data["chain"]["evolves_to"]):
        for evo in data["chain"]["evolves_to"]:
            preevol(evo, data["chain"]["species"]["name"])


def preevol(D: dict, preevo: str):
    strL = []
    try:
        for key in D["evolution_details"][0]:
            if D["evolution_details"][0][key] not in [None, "", False]:
                if key == "trigger":
                    trigger = D["evolution_details"][0][key]["name"]
                elif type(D["evolution_details"][0][key]) == dict:
                    strL.append(f'{key}:{D["evolution_details"][0][key]["name"]}')
                else:
                    strL.append(f'{key}:{D["evolution_details"][0][key]}')
            strT = "__".join(strL)
        evolutionL.append(
            (pokemonD[preevo].id, pokemonD[D["species"]["name"]].id, trigger, strT)
        )
        if len(D["evolves_to"]):
            preevol(D["evolves_to"][0], D["species"]["name"])
    except KeyError:
        return
    except IndexError:
        return


attribute = [
    "move",
    "pokemon",
    "type",
    "ability",
    "evolution-chain",
]
regions = {
    "151": "kanto",
    "251": "jotho",
    "386": "hoen",
    "493": "sinnoh",
    "649": "teselia",
    "721": "kalos",
    "809": "alola",
    "905": "galar",
}
pokemonD = {}
moveD = {}
abilityD = {}
typeD = {}

db = MySQLdb.connect(  # esto hace la conexion a la base de datos
    host="localhost",  # el puerto es 3308 porque es el puerto que
    user="root",  # le deje a mariaDB
    password="zamromxd",
    database="PokeSearch",
    port=3308,
)
start = time.time()
for i in range(1,19):                                                                          #Add all Types
    t = Type(f"https://pokeapi.co/api/v2/type/{i}/")                                           #to DB
    typeD[t.name] = t

typePrimary = [(typeD[tipe].id, typeD[tipe].name) for tipe in typeD]
damage_relations = []

for tipe in typeD:
    for dmr in typeD[tipe].damage_relations:
        for t in typeD[tipe].damage_relations[dmr]:
            damage_relations.append((typeD[tipe].id, dmr, typeD[t].id))

for i in range(1, 906):
    poke = Pokemon(f"https://pokeapi.co/api/v2/pokemon/{i}")
    pokemonD[poke.name] = poke
    for a in poke.abilities:
        if a not in abilityD:
            ability = Ability(f"https://pokeapi.co/api/v2/ability/{a}")
            abilityD[a] = ability
    for m in poke.moves:
        if m not in moveD:
            move = Move(f"https://pokeapi.co/api/v2/move/{m}")
            moveD[m] = move
    if str(i) in regions:
        print(f"{regions[str(i)]} lista")
        print(time.time() - start)

evolutionL = []
for i in range(1, 542):
    if i not in [210, 222, 225, 226, 227, 231, 238, 251]:
        evoChain(f"https://pokeapi.co/api/v2/evolution-chain/{i}")

pokeL = []
for p in pokemonD:
    pokeL.append(
        (
            pokemonD[p].id,
            pokemonD[p].name,
            pokemonD[p].weight,
            pokemonD[p].height,
            pokemonD[p].stats["hp"],
            pokemonD[p].stats["attack"],
            pokemonD[p].stats["defense"],
            pokemonD[p].stats["special-attack"],
            pokemonD[p].stats["special-defense"],
            pokemonD[p].stats["speed"],
        )
    )


pokeType = []
for p in pokemonD:
    p_id = pokemonD[p].id
    for t in pokemonD[p].types:
        pokeType.append((p_id, typeD[t].id))

abilityL = []
for a in abilityD:
    abilityL.append((abilityD[a].id, abilityD[a].name, abilityD[a].effect_entries))

pokeAbility = []
for p in pokemonD:
    p_id = pokemonD[p].id
    for a in pokemonD[p].abilities:
        pokeAbility.append((p_id, abilityD[a].id))

moveL = []
for m in moveD:
    moveL.append(
        (
            moveD[m].id,
            moveD[m].name,
            typeD[moveD[m].tipe].id,
            moveD[m].damage_class,
            moveD[m].power,
            moveD[m].pp,
            moveD[m].accuracy,
            moveD[m].priority,
            moveD[m].ailment,
            moveD[m].effect_chance,
            moveD[m].effect_entries,
        )
    )

pokeMove = []
for p in pokemonD:
    p_id = pokemonD[p].id
    for m in pokemonD[p].moves:
        pokeMove.append((p_id, moveD[m].id))

c = db.cursor()
c.executemany("INSERT INTO tipe (id,name) VALUES (%s,%s);", typePrimary)

c.executemany(
    "INSERT INTO relation_type (id_type_1,relation,id_type_2) VALUES (%s,%s,%s)",
    damage_relations,
)
c.executemany(
    "INSERT INTO pokemon (id,name,weight,height,hp,atk,def,satk,sdef,spe) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
    pokeL,
)
c.executemany(
    "INSERT INTO evolution (id_preevo,id_evol,method,details) VALUES (%s,%s,%s,%s);",
    evolutionL,
)
c.executemany("INSERT INTO pok_typ (id_pokemon,id_type) VALUES (%s,%s);", pokeType)
c.executemany("INSERT INTO ability (id,name,effect) VALUES (%s,%s,%s);", abilityL)
c.executemany(
    "INSERT INTO pok_abi (id_pokemon,id_ability) VALUES (%s,%s);", pokeAbility
)
c.executemany(
    "INSERT INTO move (id,name,id_type,damage_class,power,pp,accuracy,priority,ailment,effect_chance,effect_entries) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
    moveL,
)
c.executemany("INSERT INTO pok_mov (id_pokemon,id_move) VALUES (%s,%s);", pokeMove)
db.commit()
db.close()
