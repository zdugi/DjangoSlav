from django.contrib import admin
from interface.models import Experiment
from interface.models import Tokeni
from interface.models import PravaPristupa

class ExperimentAdmin(admin.ModelAdmin):
    list_display = ( 'naziv', 'apikey', 'adresa', 'datum_kreiranja')
    
    def get_form(self, request, obj=None, **kwargs):
        if obj: # ako je obj not none onda je edit strana
            kwargs['exclude'] = ['apikey', 'broj_pregleda',]
        else: # ako je obj none onda je add strana
            kwargs['fields'] = ['naziv', 'adresa', 'port', 'opis', 'datum_kreiranja', 'demo_video']
        return super(ExperimentAdmin, self).get_form(request, obj, **kwargs)
    
    # ovo sam stavio jer readonly polja ne mogu da se sakriju
    # pa sam preko ove funkcije ispitivao
    
    def get_readonly_fields(self, request, obj=None):
        if obj: # ako je obj not none onda je edit strana
            return ['apikey', 'broj_pregleda',]
        else: # ako je obj none onda je add strana
            return []
            
admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(Tokeni)
admin.site.register(PravaPristupa)

