import MySQLdb


class Pokemon:
    def __init__(self, name: str):
        c.execute(
            f"select id,atk,satk,def,sdef,total_stat,name from pokemon where name='{name}';"
        )
        data = c.fetchall()
        self.id = data[0][0]
        self.atk = data[0][1]
        self.defe = data[0][3]
        self.satk = data[0][2]
        self.sdef = data[0][4]
        self.total = data[0][5]
        self.name = data[0][6]
        c.execute(f"select id_type from pok_typ where id_pokemon={data[0][0]};")
        T = c.fetchall()
        self.types = []
        for t in T:
            self.types.append(t[0])
        self.damages = damages(self.types)

        self.moves = {"physical": dict(), "status": dict(), "special": dict()}
        c.execute(
            f"select M.name,M.id_type,M.damage_class from move as M inner join pok_mov as PM on  PM.id_move=M.id and PM.id_pokemon={self.id};"
        )
        M = c.fetchall()
        for att in M:
            if att[1] not in self.moves[att[2]]:
                self.moves[att[2]][att[1]] = list()
            self.moves[att[2]][att[1]].append(att[0])


def damages(T: list):
    D = dict()
    for t in T:
        for rt in relations[t]:
            for ti in relations[t][rt]:
                if ti in D:
                    if rt == "double_damage_from":
                        D[ti] *= 2
                    elif rt == "half_damage_from":
                        D[ti] *= 0.5
                    else:
                        D[ti] *= 0
                else:
                    if rt == "double_damage_from":
                        D[ti] = 2
                    elif rt == "half_damage_from":
                        D[ti] = 0.5
                    else:
                        D[ti] = 0
    return D


def cantMove(principal: Pokemon):
    cant = dict()
    for clas in principal.moves:
        cant[clas] = dict()
        for tipo in principal.moves[clas]:
            cant[clas][tipo] = len(principal.moves[clas][tipo])
    return cant


def puntaje(M: Pokemon, m_atk, o_def, O: Pokemon):
    ptM = 0
    priCant = cantMove(M)
    for classM in priCant:
        for t in priCant[classM]:
            p = priCant[classM][t]
            pp = p
            if m_atk and classM == m_atk:
                p += pp / 4
            if o_def and o_def == classM:
                p -= pp / 4
            if t in M.types:
                p += pp / 2
            if t in O.damages:
                p *= O.damages[t]
            ptM += p
    return ptM


def calcular(main: Pokemon, other: Pokemon):
    if main.atk > main.satk:
        pri_atk = "physical"
    elif main.atk < main.satk:
        pri_atk = "special"
    else:
        pri_atk = False
    if main.defe > main.sdef:
        pri_def = "physical"
    elif main.defe < main.sdef:
        pri_def = "special"
    else:
        pri_def = False
    if other.atk > other.satk:
        other_atk = "physical"
    elif other.atk < other.satk:
        other_atk = "special"
    else:
        other_atk = False
    if other.defe > other.sdef:
        other_def = "physical"
    elif other.defe < other.sdef:
        other_def = "special"
    else:
        other_def = False

    ptM = puntaje(M=main, m_atk=pri_atk, o_def=other_def, O=other)
    ptO = puntaje(M=other, m_atk=other_atk, o_def=pri_def, O=main)

    return ptM - ptO + (main.total - other.total)


def pokeSearch(p: str):
    poke = Pokemon(p)
    pokes = dict()
    c.execute(
        f"select name from pokemon where total_stat>={poke.total-20} and total_stat<={poke.total+20} and id!={poke.id};"
    )
    data = c.fetchall()
    for r in data:
        pokes[r[0]] = Pokemon(r[0])
    PL = list()
    for pp in pokes:
        PL.append((pp, calcular(poke, pokes[pp])))
        PL.sort(key=lambda x: x[1])
    return [p[0] for p in PL[0:3]], [p[0] for p in PL[-3:]]


db = MySQLdb.connect(  # esto hace la conexion a la base de datos
    host="localhost",  # el puerto es 3308 porque es el puerto que
    user="root",  # le deje a mariaDB
    password="zamromxd",
    database="PokeSearch",
    port=3308,
)
c = db.cursor()

TYPES = dict()
c.execute(f"select * from tipe;")
result = c.fetchall()
for tipe in result:
    TYPES[tipe[0]] = tipe[1]
relations = dict()
for t_id in TYPES:
    if t_id not in relations:
        relations[t_id] = dict()
    c.execute(
        f"select relation,id_type_2 from relation_type where id_type_1={t_id} and relation like '%from' ;"
    )
    temp = c.fetchall()
    for rt in temp:
        if rt[0] not in relations[t_id]:
            relations[t_id][rt[0]] = []
            relations[t_id][rt[0]].append(rt[1])
        else:
            relations[t_id][rt[0]].append(rt[1])

p = input().strip()
worst, better =pokeSearch(p)
print(worst,better)