from __future__ import unicode_literals
import random, string

from django.db import models

def create_apikey():
        key_lenght = 32
        global_key_lenght = 16
        GLOBAL = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(global_key_lenght))
        key = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(key_lenght))
        APIKEY = GLOBAL + key
        
        return APIKEY

class Experiment(models.Model):
    apikey = models.CharField(max_length=48, default=create_apikey())
    naziv = models.CharField(max_length=30)
    adresa = models.GenericIPAddressField(protocol='both', unpack_ipv4=True, null=False)
    port = models.IntegerField(null=False)
    opis = models.TextField()
    datum_kreiranja = models.DateField()

    class Meta:
        verbose_name = "Eksperiment"
        verbose_name_plural = "Eksperimenti"
    
    def __str__(self):
        return self.naziv
        
