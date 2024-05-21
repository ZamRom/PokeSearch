import requests
import MySQLdb
import time


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
            (pokemonD[preevo], pokemonD[D["species"]["name"]], trigger, strT)
        )
        if len(D["evolves_to"]):
            preevol(D["evolves_to"][0], D["species"]["name"])
    except KeyError:
        return
    except IndexError:
        return


db = MySQLdb.connect(  # esto hace la conexion a la base de datos
    host="localhost",  # el puerto es 3308 porque es el puerto que
    user="root",  # le deje a mariaDB
    password="zamromxd",
    database="PokeSearch",
    port=3308,
)

pokemonD = {}
cursor = db.cursor()  # recordar que esto lo estoy haciendo porque no quiero hacer el

start = time.time()
cursor.execute(
    "SELECT * FROM pokemon;"
)  # request cada vez, pero recordar que eso no son solo llaves y
results = cursor.fetchall()  # valores sino que son objetos
for p in results:
    pokemonD[p[1]] = p[0]
evolutionL = []
for i in range(1, 542):
    if i not in [210, 222, 225, 226, 227, 231, 238, 251]:
        evoChain(f"https://pokeapi.co/api/v2/evolution-chain/{i}")
        # print(i)
        if i%10==0:print(i)
        # print(evolutionL)
c = db.cursor()
c.executemany(
    "INSERT INTO evolution (id_preevo,id_evol,method,details) VALUES (%s,%s,%s,%s);",
    evolutionL,
)
db.commit()
end = time.time()
db.close()
print(end - start)
