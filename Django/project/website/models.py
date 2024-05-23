# website/models.py
from django.db import models


class Pokemon(models.Model):
    name = models.CharField(max_length=255, unique=True)
    weight = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()
    hp = models.PositiveSmallIntegerField()
    atk = models.PositiveSmallIntegerField()
    def_stat = models.PositiveSmallIntegerField()
    satk = models.PositiveSmallIntegerField()
    sdef = models.PositiveSmallIntegerField()
    spe = models.PositiveSmallIntegerField()
    total_stat = models.PositiveSmallIntegerField()
    sprite = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Tipe(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Relation(models.Model):
    relation_choices = {
        "double_damage_from": "double_damage_from",
        "double_damage_to": "double_damage_to",
        "half_damage_from": "half_damage_from",
        "half_damage_to": "half_damage_to",
        "no_damage_from": "no_damage_from",
        "no_damage_to": "no_damage_to",
    }
    id_1 = models.ForeignKey(Tipe, on_delete=models.CASCADE, related_name="id_attacker")
    relation = models.CharField(
        max_length=18,
        choices=relation_choices,
    )
    id_2 = models.ForeignKey(Tipe, on_delete=models.CASCADE, related_name="id_defensor")

    def __str__(self):
        return str(self.relation)


class Ability(models.Model):
    name = models.CharField(max_length=255, unique=True)
    effect = models.CharField(max_length=1500)

    def __str__(self):
        return self.name


class Move(models.Model):
    name = models.CharField(max_length=255, unique=True)
    id_type = models.ForeignKey(Tipe, on_delete=models.CASCADE)
    class_choices = {"physical": "physical", "special": "special", "status": "status"}
    damage_class = models.CharField(
        max_length=8,
        choices=class_choices,
    )
    power = models.PositiveSmallIntegerField(null=True)
    pp = models.PositiveSmallIntegerField()
    accuracy = models.PositiveSmallIntegerField(null=True)
    priority = models.SmallIntegerField(null=True)
    aliment = models.CharField(max_length=255,null=True)
    effect_chance = models.PositiveSmallIntegerField(null=True)
    effect_entries = models.CharField(max_length=2600,null=True)

    def __str__(self):
        return self.name


class Evolution(models.Model):
    id_preevo = models.ForeignKey(
        Pokemon, on_delete=models.CASCADE, related_name="id_preevo"
    )
    id_evo = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="id_evo")
    method = models.CharField(max_length=255)
    details = models.CharField(max_length=511)

    def __str__(self):
        return f"{self.id_preevo} to {self.id_evo}"


class Pok_typ(models.Model):
    id_pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    id_type = models.ForeignKey(Tipe, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_type)


class Pok_mov(models.Model):
    id_pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    id_move = models.ForeignKey(Move, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id_move}"


class Pok_abi(models.Model):
    id_pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    id_ability = models.ForeignKey(Ability, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id_pokemon} has {self.id_ability}"
