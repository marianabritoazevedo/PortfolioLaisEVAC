from django.contrib import admin
from autocompletefilter.admin import AutocompleteFilterMixin
from autocompletefilter.filters import AutocompleteListFilter
from .models import Vacina, Estabelecimento, UF, Municipio, Profissional, Paciente, PacienteVacina, Agenda, HorarioAgenda, Estoque 

# Register your models here.
class VacinaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
    list_per_page = 5

#class VacinaFilter(AutocompleteFilter.ModelAdmin):
    #title = 'Vacina' # display title
    #field_name = 'nome' # name of the foreign key field

class EstabelecimentoAdmin(admin.ModelAdmin):
    list_display = ('razaoSocial','nomeFantasia')
    search_fields = ('nomeFantasia',)

class UFAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

class MunicipioAdmin(AutocompleteFilterMixin, admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
    list_filter = (
        ('uf', AutocompleteListFilter),
    )
    list_per_page = 15

class ProfissionalAdmin(AutocompleteFilterMixin, admin.ModelAdmin):
    list_display = ('nome','estabelecimento','user')
    search_fields = ('nome',)
    list_filter = (
        ('estabelecimento', AutocompleteListFilter),
    )

class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

class AgendaAdmin(AutocompleteFilterMixin, admin.ModelAdmin):
    date_hierarchy = 'data'
    search_fields = ('data','estabelecimento',)
    list_filter = (
        ('estabelecimento', AutocompleteListFilter),
    )

class EstoqueAdmin(admin.ModelAdmin):
    list_display = ('vacina', 'quantidade', 'estabelecimento',)


admin.site.register(Vacina, VacinaAdmin)
admin.site.register(Estabelecimento, EstabelecimentoAdmin)
admin.site.register(UF, UFAdmin)
admin.site.register(Municipio, MunicipioAdmin)
admin.site.register(Profissional, ProfissionalAdmin)
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(PacienteVacina)
admin.site.register(Agenda, AgendaAdmin)
admin.site.register(HorarioAgenda)
admin.site.register(Estoque, EstoqueAdmin)
