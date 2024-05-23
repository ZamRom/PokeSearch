from django.contrib import admin
from .models import Pokemon

@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight', 'height', 'hp', 'atk', 'def_stat', 'satk', 'sdef', 'spe', 'sprite')
    search_fields = ('name',)
    ordering = ('id',)

    # No incluyas el campo 'id' en los formularios de creación o edición
    fields = ('name', 'weight', 'height', 'hp', 'atk', 'def_stat', 'satk', 'sdef', 'spe', 'sprite')

# No necesitas crear un formulario personalizado si no tienes requisitos específicos.
