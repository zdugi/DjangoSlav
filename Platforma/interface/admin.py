from django.contrib import admin

from .models import Experiment

class ExperimentAdmin(admin.ModelAdmin): 
    list_display = ('naziv', 'adresa', 'datum_kreiranja')
    readonly_fields=('apikey',)

admin.site.register(Experiment, ExperimentAdmin)
