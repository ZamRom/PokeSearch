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


class Type:
    def __init__(self, link):
        data = requests.get(link).json()
        self.id = data["id"]
        self.name = data["name"]
        self.damage_relations = {}
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
        try:
            if len(self.effect_entries) > 1560:
                print(
                    f"\t\t\t\t\t\tWARNING WITH {self.name}({self.id}) len:{len(self.effect_entries)}"
                )
        except AttributeError:
            self.effect_entries = ""
            # print(f"\t\t\t\t\t\tWARNING WITH {self.name}({self.id})")

    def print(self):
        print(f"Id            : {self.id}")
        print(f"Name          : {self.name}")
        print(f"Effect_entries: {self.effect_entries}")


db = MySQLdb.connect(  # esto hace la conexion a la base de datos
    host="localhost",  # el puerto es 3308 porque es el puerto que
    user="root",  # le deje a mariaDB
    password="zamromxd",
    database="PokeSearch",
    port=3308,
)

typeD = {}

pokemonD = {}
moveD = {}
abilityD = {}

cursor = db.cursor()  # recordar que esto lo estoy haciendo porque no quiero hacer el

cursor.execute(
    "SELECT * FROM tipe;"
)                    # request cada vez, pero recordar que eso no son solo llaves y
results = cursor.fetchall()  # valores sino que son objetos
for t in results:
    typeD[t[1]] = t[0]

kanto = (1, 152)
jotho = (152, 252)
hoen = (252, 387)
sinnoh = (387,494)
teselia = (494,650)
kalos = (450,722)
alola = (722,810)
galar = (810,906)
forms = (1026,1254)
regions = {
    '151':'kanto',
    '251': 'jotho',
    '386':'hoen',
    '493':'sinnoh',
    '649':'teselia',
    '721':'kalos',
    '809':'alola',
    '905':'galar'
    }
start = time.time()

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
        pokeType.append((p_id, typeD[t]))

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
            typeD[moveD[m].type],
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
c.executemany(
    "INSERT INTO pokemon (id,name,weight,height,hp,atk,def,satk,sdef,spe) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
    pokeL,
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
end = time.time()
print(end - start)
