# Create your models here.
from django.db import models


class Ville(models.Model):
    nom = models.CharField(max_length=100)
    code_postal = models.IntegerField()
    prix_m_2 = models.IntegerField()

    def __str__(self):
        return self.nom


class Local(models.Model):
    nom = models.CharField(max_length=100)
    ville = models.ForeignKey(Ville, on_delete=models.PROTECT)
    surface = models.IntegerField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.nom


class SiegeSocial(Local):
    president = models.CharField(max_length=100)


class Machine(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.IntegerField()
    n_serie = models.IntegerField()

    def __str__(self):
        return self.nom


class Usine(Local):
    machines = models.ManyToManyField(Machine)


class Objet(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.IntegerField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.nom


class Ressource(Objet):
    def __str__(self):
        return self.nom


class QuantiteRessource(models.Model):
    ressource = models.ForeignKey(Ressource, on_delete=models.CASCADE)
    quantite = models.IntegerField()


class Etape(models.Model):
    nom = models.CharField(max_length=100)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    quantite_ressource = models.ForeignKey(QuantiteRessource, on_delete=models.PROTECT)
    duree = models.IntegerField()
    etape_suivante = models.ForeignKey(
        "self", null=True, on_delete=models.CASCADE, blank=True
    )

    def __str__(self):
        return self.nom


class Stock(models.Model):
    ressource = models.ForeignKey(Ressource, on_delete=models.CASCADE)
    nombre = models.IntegerField()


class Produit(Objet):
    premiere_etape = models.ForeignKey(Etape, on_delete=models.CASCADE)
