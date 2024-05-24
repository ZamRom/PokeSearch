import sqlite3
import MySQLdb

db = MySQLdb.connect(
    host="localhost",
    user="root",
    password="zamromxd",
    database="PokeSearch",
    port=3308,
)

DB = sqlite3.connect("db.sqlite3")
C = DB.cursor()
c = db.cursor()

C.execute("delete from website_pokemon;")
C.execute("delete from website_tipe;")
C.execute("delete from website_relation;")
C.execute("delete from website_pok_typ;")
C.execute("delete from website_pok_mov;")
C.execute("delete from website_pok_abi;")
C.execute("delete from website_ability;")
C.execute("delete from website_move;")
C.execute("delete from website_evolution;")


c.execute("select * from tipe;")
data = c.fetchall()
C.executemany("insert into website_tipe values (?,?)", data)

c.execute("select * from relation_type;")
data = c.fetchall()
C.executemany(
    "INSERT INTO website_relation (id_1_id,relation,id_2_id) VALUES (?,?,?)",
    data,
)

c.execute(
    "select id,name,weight,height,hp,atk,def,satk,sdef,spe,total_stat,sprite from pokemon;"
)
data = c.fetchall()
C.executemany(
    "INSERT INTO website_pokemon (id,name,weight,height,hp,atk,def_stat,satk,sdef,spe,total_stat,sprite) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
    data,
)

c.execute("select * from evolution;")
data = c.fetchall()
C.executemany(
    "INSERT INTO website_evolution (id_preevo_id,id_evo_id,method,details) VALUES (?,?,?,?);",
    data,
)

c.execute("select * from pok_typ;")
data = c.fetchall()
C.executemany("INSERT INTO website_pok_typ (id_pokemon_id,id_type_id) VALUES (?,?);", data)

c.execute("select * from ability;")
data = c.fetchall()
C.executemany("INSERT INTO website_ability  VALUES (?,?,?);", data)

c.execute("select * from pok_abi;")
data = c.fetchall()
C.executemany("INSERT INTO website_pok_abi (id_pokemon_id,id_ability_id) VALUES (?,?);", data)

c.execute("select * from move;")
data = c.fetchall()
C.executemany(
    "INSERT INTO website_move (id,name,id_type_id,damage_class,power,pp,accuracy,priority,aliment,effect_chance,effect_entries) VALUES (?,?,?,?,?,?,?,?,?,?,?);",
    data,
)

c.execute("select * from pok_mov;")
data = c.fetchall()
C.executemany("INSERT INTO website_pok_mov (id_pokemon_id,id_move_id) VALUES (?,?);", data)

DB.commit()
C.close()
DB.close()
c.close()
db.close()
