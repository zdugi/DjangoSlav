from __future__ import unicode_literals
import random, string

from django.db import models
from django.contrib.auth.models import User

def create_apikey():
        key_lenght = 32
        global_key_lenght = 16
        GLOBAL = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(global_key_lenght))
        key = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(key_lenght))
        APIKEY = GLOBAL + key
        
        return APIKEY

class Experiment(models.Model):
        apikey = models.CharField(max_length=48, unique=True, null=False)
        naziv = models.CharField(max_length=30, null=False)
        adresa = models.GenericIPAddressField(protocol='both', unpack_ipv4=True, null=False)
        port = models.IntegerField(null=False)
        opis = models.TextField()
        datum_kreiranja = models.DateField(null=False)
        demo_video = models.CharField(max_length=200, null=True, blank=True)
        broj_pregleda = models.PositiveIntegerField(default=0, null=False)

        def save(self):
                if not self.id:
                        self.apikey = create_apikey()
                super(Experiment, self).save()

        def __str__(self):
                return self.naziv

        class Meta:
                verbose_name = "Eksperiment"
                verbose_name_plural = "Eksperimenti"
        

class Tokeni(models.Model):
        user_id = models.ForeignKey(User, on_delete=models.CASCADE)
        eksperiment_id = models.ForeignKey(Experiment, on_delete=models.CASCADE)
        startVreme = models.DateTimeField(null=False)
        endVreme = models.DateTimeField(null=False)
        token = models.CharField(max_length = 56, null = False)

        class Meta:
                verbose_name = "Token"
                verbose_name_plural = "Tokeni"

class PravaPristupa(models.Model):
        user_id = models.ForeignKey(User, on_delete=models.CASCADE)
        eksperiment_id = models.ForeignKey(Experiment, on_delete=models.CASCADE)

        class Meta:
                verbose_name = "Pravo pristupa"
                verbose_name_plural = "Prava pristupa"


class Poruke(models.Model):
        sadrzaj = models.TextField()
        odgovor = models.BooleanField(null=False, default=False)
        datum_slanja = models.DateTimeField(null=False)
        user_id = models.ForeignKey(User, on_delete=models.CASCADE)

        class Meta:
                verbose_name = "Poruka"
                verbose_name_plural = "Poruke"

