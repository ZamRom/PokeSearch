# Librerías y moulos
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404,get_list_or_404
from django.http import JsonResponse
from .models import Pok_typ,Pok_mov,Move, Pokemon,Tipe,Relation


class Pok:
    def __init__(self, pokemon_name: str):
        # Obtenemos los datos del Pokemon
        data = get_object_or_404(Pokemon, name__iexact=pokemon_name)
        # Inicializamos los atributos del objeto Pok
        self.id = data.id
        self.atk = data.atk
        self.defe = data.def_stat
        self.satk = data.satk
        self.sdef = data.sdef
        self.total = data.total_stat
        self.name = data.name
        # Obtenemos los tipos del Pokemon
        T = get_list_or_404(Pok_typ, id_pokemon_id=data.id)
        self.types = []
        for t in T:
            # Añadimos los tipos a la lista de tipos del Pokemon
            self.types.append(get_object_or_404(Tipe,name=t).id)
        # Calculamos los daños del Pokemon
        self.damages = damages(self.types)

        # Inicializamos el diccionario de movimientos del Pokemon
        self.moves = {"physical": dict(), "status": dict(), "special": dict()}
        # Obtenemos los movimientos del Pokemon
        Mov = get_list_or_404(Pok_mov, id_pokemon_id=self.id)
        for m in Mov:
            M = get_object_or_404(Move, name=m)
            if M.id_type_id not in self.moves[M.damage_class]:
                self.moves[M.damage_class][M.id_type_id] = list()
            self.moves[M.damage_class][M.id_type_id].append(M.name)

# Calcula los daños causados por un tipo de Pokémon contra otros tipos.
def damages(T: list):                               # T (list): Lista de identificadores de tipo de Pokémon.
    D = dict()                                      # Un diccionario que mapea identificadores de tipo a los multiplicadores de daño.
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

# Crea las relaciones entre tipos de Pokémon.
def createR():
    global TYPES
    global relations
    TYPES = dict()
    relations = dict()

    # Obtenemos los tipos de Pokémon y los almacenamos en un diccionario
    for i in range(1,19):
        t = get_object_or_404(Tipe,id=i)
        TYPES[t.id] = t.name

    # Creamos las relaciones entre tipos de Pokémon
    for t_id in TYPES:
        RT = get_list_or_404(Relation,id_1_id=t_id,relation__endswith='from')
        for rt in RT:
            if t_id not in relations:
                relations[t_id] = dict()
            if rt.relation not in relations[t_id]:
                relations[t_id][rt.relation] = []
                relations[t_id][rt.relation].append(rt.id_2_id)
            else:
                relations[t_id][rt.relation].append(rt.id_2_id)


def cantMove(principal: Pok):
    """
    Calcula la cantidad de movimientos disponibles para cada clase de movimiento de un Pokémon.
    
    Args:
        principal (Pok): Instancia del Pokémon del que se desea calcular la cantidad de movimientos.
        
    Returns:
        dict: Un diccionario que mapea clases de movimientos a la cantidad de movimientos disponibles para cada tipo.
    """
    cant = dict()
    for clas in principal.moves:
        cant[clas] = dict()
        for tipo in principal.moves[clas]:
            cant[clas][tipo] = len(principal.moves[clas][tipo])
    return cant


def puntaje(M: Pok, m_atk, o_def, O: Pok):
    """
    - Calcula el puntaje de un Pokémon en base a sus movimientos, tipos y atributos comparado con otro Pokémon. 
    Args:
        M (Pok): Instancia del Pokémon para el que se calculará el puntaje.
        m_atk (str): Clase de movimiento de ataque del Pokémon M.
        o_def (str): Clase de movimiento de defensa del Pokémon O.
        O (Pok): Instancia del otro Pokémon con el que se compara.       
    Returns:
        float: El puntaje calculado para el Pokémon M en relación con el Pokémon O.
    """
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


def calcular(main: Pok, other: Pok):
    """
    Calcula el puntaje de comparación entre dos Pokémon.
    Args:
        main (Pok): Instancia del Pokémon principal.
        other (Pok): Instancia del otro Pokémon con el que se compara.

    Returns:
        float: El puntaje de comparación entre los dos Pokémon.
    """
    # Determina la clase de movimiento de ataque del Pokémon principal
    if main.atk > main.satk:
        pri_atk = "physical"
    elif main.atk < main.satk:
        pri_atk = "special"
    else:
        pri_atk = False
    
    # Determina la clase de movimiento de defensa del Pokémon principal
    if main.defe > main.sdef:
        pri_def = "physical"
    elif main.defe < main.sdef:
        pri_def = "special"
    else:
        pri_def = False

    # Determina la clase de movimiento de ataque del otro Pokémon
    if other.atk > other.satk:
        other_atk = "physical"
    elif other.atk < other.satk:
        other_atk = "special"
    else:
        other_atk = False

    # Determina la clase de movimiento de defensa del otro Pokémon
    if other.defe > other.sdef:
        other_def = "physical"
    elif other.defe < other.sdef:
        other_def = "special"
    else:
        other_def = False

    # Calcula el puntaje para el Pokémon principal y el otro Pokémon
    ptM = puntaje(M=main, m_atk=pri_atk, o_def=other_def, O=other)
    ptO = puntaje(M=other, m_atk=other_atk, o_def=pri_def, O=main)

    # Calcula el puntaje final restando los puntajes y sumando la diferencia total de estadísticas
    return ptM - ptO + (main.total - other.total)


def pokeSearch(p: str):
    """
    Busca los Pokémon más similares al Pokémon dado.
    Args:
        p (str): Nombre del Pokémon a buscar.
    Returns:
        tuple: Una tupla que contiene dos listas. La primera lista contiene los nombres de los tres Pokémon más
               similares al Pokémon dado, y la segunda lista contiene los nombres de los tres Pokémon menos similares.
    """
    # Crea una instancia del Pokémon dado
    poke = Pok(p)
    # Inicializa un diccionario para almacenar los Pokémon's encontrados
    pokes = dict()

    # Obtiene los Pokémon cuyas estadísticas totales estén dentro de un rango cercano al del Pokémon dado
    data = get_list_or_404(Pokemon, total_stat__gte=poke.total - 20, total_stat__lte=poke.total + 20)
    # Itera sobre los Pokémon encontrados
    for r in data:
        # Verifica que el Pokémon no sea el mismo que el dado
        if r.name != poke.name:
            # Agrega el Pokémon al diccionario de Pokémon encontrados
            pokes[r.name] = Pok(r.name)

    # Inicializa una lista para almacenar los Pokémon junto con sus puntajes de similitud
    PL = list()
    # Calcula el puntaje de similitud entre el Pokémon dado y los Pokémon encontrados, y los agrega a la lista PL
    for pp in pokes:
        PL.append((pp, calcular(poke, pokes[pp])))
        # Ordena la lista PL por puntaje de similitud
        PL.sort(key=lambda x: x[1])
    # Retorna las tres primeras y tres últimas entradas de la lista PL, que corresponden a los Pokémon más y menos similares
    return [p[0] for p in PL[0:3]], [p[0] for p in PL[-3:]]


def buscar_pokemon(request):
    # Obtiene el parámetro 'query' de la solicitud, que representa el nombre del Pokémon a buscar
    query = request.GET.get('query', '')
    if query:
        try:
            pokemon = Pokemon.objects.get(name__iexact=query)
        except Pokemon.DoesNotExist:
            return JsonResponse({'error': 'Pokémon no encontrado.'}, status=404)
        
        # Si se encuentra el Pokémon, crea un diccionario con el nombre del Pokémon encontrado
        data = {
            'name': pokemon.name
        }
        # Retorna una respuesta JSON con el nombre del Pokémon encontrado
        return JsonResponse(data)

def detalle_pokemon(request, pokemon_name):
    # Diccionario que mapea los tipos a colores
    tipo_colores = {
        'electric': '#FFEB3B',  # amarillo pastel
        'fire': '#FF8A65',  # rojo pastel
        'water': '#64B5F6',  # azul pastel
        'grass': '#81C784',  # verde claro pastel
        'ice': '#81D4FA',  # azul claro pastel
        'fighting': '#FFAB91',  # marrón claro pastel
        'poison': '#CE93D8',  # púrpura pastel
        'ground': '#D7CCC8',  # beige pastel
        'flying': '#B3E5FC',  # celeste pastel
        'psychic': '#FFC1E3',  # rosa pastel
        'bug': '#C5E1A5',  # verde pastel
        'rock': '#A1887F',  # marrón claro pastel
        'ghost': '#B39DDB',  # índigo pastel
        'dragon': '#7986CB',  # azul oscuro pastel
        'dark': '#90A4AE',  # gris claro pastel
        'steel': '#CFD8DC',  # gris muy claro
        'fairy': '#F48FB1',  # rosa claro pastel
    }
    createR()
    pokemon = get_object_or_404(Pokemon, name__iexact=pokemon_name)
    types = get_list_or_404(Pok_typ, id_pokemon_id=pokemon.id)
    pokemon.type = list()
    for t in types:
        pokemon.type.append(get_object_or_404(Tipe, name=t).name)
    
    # Obtener el color según el primer tipo del Pokémon
    main_type = pokemon.type[0]
    pokemon.color = tipo_colores.get(main_type, '#FFFFFF')  # Color blanco por defecto

    data = pokeSearch(pokemon_name)
    worst = []
    better = []
    for c in data:
        for against in c:
            if c == data[0]:
                p = get_object_or_404(Pokemon, name__iexact=against)
                types = get_list_or_404(Pok_typ, id_pokemon_id=p.id)
                p.type = list()
                for t in types:
                    p.type.append(get_object_or_404(Tipe, name=t).name)
                
                # Obtener el color según el primer tipo del Pokémon
                main_type = p.type[0].lower()
                p.color = tipo_colores.get(main_type, '#FFFFFF')
                
                worst.append(p)
            else:
                p = get_object_or_404(Pokemon, name__iexact=against)
                types = get_list_or_404(Pok_typ, id_pokemon_id=p.id)
                p.type = list()
                for t in types:
                    p.type.append(get_object_or_404(Tipe, name=t).name)
                
                # Obtener el color según el primer tipo del Pokémon
                main_type = p.type[0].lower()
                p.color = tipo_colores.get(main_type, '#FFFFFF')
                
                better.append(p)

    context = {
        'pokemon': pokemon,
        'worst': worst,
        'better': better 
    }
    return render(request, 'detalle.html', context)

def inicio(request):
    '''
    Función que muestra la vista de la página de inicio
    '''
    return render(request, 'home.html')

def pokemon(request):
    if request.method == 'POST':
        return render(request, 'base.html')
