import requests
import MySQLdb
import re

"""
with open("PokeSearch/KantoPokemon.txt", "w+") as file:
    file.write("Pokemon de Kanto")
    link = "https://pokeapi.co/api/v2/pokemon/?limit=1302"
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
attribute = [
    "move",
    "pokemon",
    "type",
    "ability",
    "evolution-chain",
]


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
            self.effect_entries = self.effect_entries.replace('\n',' ')
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

"""
evolutionD = {}
move = Move("https://pokeapi.co/api/v2/move/tera-blast/")  # fire_punch (7) tri-attack (161) swords-dance (14)
move.print()
link = f"https://pokeapi.co/api/v2/{attribute[4]}/1"
# respt = requests.get(link).json()
evoChain(link)
"""
"""
for i in range(1,30):
    print(f'id: {i}')
    link = f"https://pokeapi.co/api/v2/{attribute[0]}/{i}"
    move = Move(link)
    move.print()
    print()
"""

db = MySQLdb.connect(  # esto hace la conexion a la base de datos
    host="localhost",  # el puerto es 3308 porque es el puerto que
    user="root",  # le deje a mariaDB
    password="zamromxd",
    database="PokeSearch",
    port=3308,
)
move = Move("https://pokeapi.co/api/v2/move/tera-blast/")  # fire_punch (7) tri-attack (161) swords-dance (14)
"""
c = db.cursor()  # no se exactamente que es un cursor, pero jala
c.execute("INSERT INTO users (name, email) VALUES ('John Doe', 'johndoe@example.com');")
db.commit()  # nunca olvidar el commit porque si lo haces no sube nada
cursor = db.cursor()
cursor.execute("SELECT * FROM users;")
results = cursor.fetchall()
print(results)
db.close()  # tampoco olvidar cerrar la conexion
"""
