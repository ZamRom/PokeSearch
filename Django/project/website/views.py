# Librerías y moulos
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404,get_list_or_404
from django.http import JsonResponse
from .models import Pok_typ,Pok_mov,Move, Pokemon,Tipe,Relation


class Pok:
    def __init__(self, pokemon_name: str):
        data = get_object_or_404(Pokemon, name__iexact=pokemon_name)
        self.id = data.id
        self.atk = data.atk
        self.defe = data.def_stat
        self.satk = data.satk
        self.sdef = data.sdef
        self.total = data.total_stat
        self.name = data.name
        T = get_list_or_404(Pok_typ, id_pokemon_id=data.id)
        self.types = []
        for t in T:
            self.types.append(get_object_or_404(Tipe,name=t).id)
        self.damages = damages(self.types)

        self.moves = {"physical": dict(), "status": dict(), "special": dict()}
        Mov = get_list_or_404(Pok_mov, id_pokemon_id=self.id)
        for m in Mov:
            M = get_object_or_404(Move, name=m)
            if M.id_type_id not in self.moves[M.damage_class]:
                self.moves[M.damage_class][M.id_type_id] = list()
            self.moves[M.damage_class][M.id_type_id].append(M.name)


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

def createR():
    global TYPES
    global relations
    TYPES = dict()
    relations = dict()

    for i in range(1,19):
        t = get_object_or_404(Tipe,id=i)
        TYPES[t.id] = t.name

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
    cant = dict()
    for clas in principal.moves:
        cant[clas] = dict()
        for tipo in principal.moves[clas]:
            cant[clas][tipo] = len(principal.moves[clas][tipo])
    return cant


def puntaje(M: Pok, m_atk, o_def, O: Pok):
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
    poke = Pok(p)
    pokes = dict()
    data = get_list_or_404(Pokemon, total_stat__gte=poke.total - 20, total_stat__lte=poke.total + 20)
    for r in data:
        if r.name != poke.name:
            pokes[r.name] = Pok(r.name)
    PL = list()
    for pp in pokes:
        PL.append((pp, calcular(poke, pokes[pp])))
        PL.sort(key=lambda x: x[1])
    return [p[0] for p in PL[0:3]], [p[0] for p in PL[-3:]]


def buscar_pokemon(request):
    query = request.GET.get('query', '')
    if query:
        try:
            pokemon = Pokemon.objects.get(name__iexact=query)
        except Pokemon.DoesNotExist:
            try:
                pokemon = Pokemon.objects.get(name=query)
            except Pokemon.DoesNotExist:
                return JsonResponse({'error': 'Pokémon no encontrado.'}, status=404)
        
        data = {
            'name': pokemon.name
        }
        return JsonResponse(data)
    return JsonResponse({'error': 'Parámetro de búsqueda no proporcionado.'}, status=400)


def detalle_pokemon(request, pokemon_name):
    createR()

    pokemon = get_object_or_404(Pokemon, name__iexact=pokemon_name)
    types = get_list_or_404(Pok_typ, id_pokemon_id=pokemon.id)
    pokemon.type = [get_object_or_404(Tipe, id=t.id_type_id).name for t in types]

    data = pokeSearch(pokemon_name)
    worst = []
    better = []

    for c in data:
        for against in c:
            p = get_object_or_404(Pokemon, name__iexact=against)
            types = get_list_or_404(Pok_typ, id_pokemon_id=p.id)
            p.type = [get_object_or_404(Tipe, id=t.id_type_id).name for t in types]

            if c == data[0]:
                worst.append(p)
            else:
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
        return render(request, 'pokemon.html')
