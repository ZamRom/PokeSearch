# PokeSearch

## Contactos

Carlos Daniel Camilo Aguilar - camilodani065@gmail.com

Ariel Rodolfo Zarmudio Romero- zamromxd@gmail.com

Humberto Cortez Vázquez - tejedordealas@gmail.com

## Licencia

PokeSearch es distribuido bajo la licencia MIT.

## Descripción

PokeSearch será un microservicio gratuito y de codigo abierto que proporcinará datos de manera accesible sobre Pokémon. Este microservicio cubre informacion util sobre pokemon, sus habilidades, tipos, evoluciones y movimientos, lo que lo hace una herramienta para jugadores novatos o aquellos usuarios que quieren iniciar con la saga principal de Pokémon.

## Justificación

Se encontró que es complicado para jugadores que no han tenido un acercamiento a los juegos estilo RPG o TBS tienen ciertas dificultades en entender el sistema de combate o sus relaciones entre 'stats' con respecto a los ataques y pokemon por lo que se desarrolla este microservicio planeando que para estos usuarios sea mas sencillo tener este acercamiento hacia los pokemon y sus relaciones par que no tengan problemas para iniciar a jugar la saga principal de Pokémon

## Características

- **Datos utiles sobre Pokémon:** Acceso a información sobre más de 800 Pokémon, incluyendo estadísticas, tipos, habilidades y más.
- **Información sobre movimientos y habilidades:** Datos detallados sobre los movimientos que pueden aprender los Pokémon y las habilidades que poseen.
- **Evoluciones:** Información detallada sobre las condiciones de evolución de los Pokémon.
- **Acceso fácil y rápido:** Diseñada con el objetivo de ser fácil de usar y con respuestas rápidas para mejorar la experiencia del usuario.

## Objetivos

- **Objetivo general:** A partir de la base de datos que se hará con los datos obtenidos de la pokeAPI poder presentar una lista de 6 pokemon que tengan afinidad buena y mala con el pokemon dado por el usuario (3 y 3) y poder brindar informacion de los pokemon que se retornan
- **Objetivos particulares:**
  -Obtener pokemon similares en stats y tipo
  -Obtener pokemon similares por tipos y cantidades de ataques que aprenden
  -Brindar informacion UTIL sobre los pokemon retornados

## Hipotesis

Dadas las stats, tipo, cantidad de ataques y sus tipos del pokemon dado por el usuario desarrollar un algoritmo que permita obtener pokemones similares en stats y tipo, otro que permita obtener similares en base a los ataques y sus tipos, para al final hacer un algoritmo que use los 2 anteriores para delimitar cuales pokemon son los mas similares dados los datos retornados y discernir cuales pokemon sería mejor que el usuario obtuviera su informacion para desarrollar estrategias

## Arquitectura

(Arquitectura: Adquisición, Almacenamiento, Procesamiento y Publicación)
**Adquisición:** La adquisicion de informacion sera por medio de python con el modulo request hacia la API de 'PokeAPI' para hacer un rapido discermiento entre informacion util y la no util para nosotros (no existe la informacion inutil).
**Almacenamiento:** La informacion obtenida y limpiada con Python será guardada en una base de datos relacional para no tener que hacer todas las request cada vez que un usuario se conecte al microservicio.
**Procesamiento:** Una vez que el usuario se conecte al microservicio y de el nombre de un pokemon hacer el uso de los 3 algoritmos para procesar la informacion y retornar al usuario solo la informacion que necesita sobre los pokemon retornados.
**Publicación:** Apartado en desarrollo\*

## Herramientas a utilizar

[Python](https://docs.python.org/release/3.10.6/) (v3.10.6) se usará como principal lenguaje para el desarrollo de los algoritmos mas la adicion de los modulos de [request](https://requests.readthedocs.io/en/latest/) y [mysql](https://dev.mysql.com/doc/connector-python/en/).
Tambien se utilizará [MariaDB](https://mariadb.com/kb/en/documentation/) para la base de datos.