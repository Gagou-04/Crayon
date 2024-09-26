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
    ville = models.ForeignKey(Ville, blank=True, null=True, on_delete=models.PROTECT)
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

    def costs(self):
        return self.prix


class Usine(Local):
    machines = models.ManyToManyField(Machine)

    def costs(self):
        cout = 0
        for machine in self.machines.all():
            cout = cout + machine.costs()

        cout = cout + self.surface * self.ville.prix_m_2

        for stock in self.stock_set.all():
            cout = cout + stock.costs()

        return cout


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
    ressource = models.ForeignKey(
        Ressource, blank=True, null=True, on_delete=models.CASCADE
    )
    quantite = models.IntegerField()

    def __str__(self):
        return self.nom

    def costs(self):
        return self.quantite * self.ressource.prix


class Etape(models.Model):
    nom = models.CharField(max_length=100)
    machine = models.ForeignKey(
        Machine, blank=True, null=True, on_delete=models.CASCADE
    )
    quantite_ressource = models.ForeignKey(
        QuantiteRessource, blank=True, null=True, on_delete=models.PROTECT
    )
    duree = models.IntegerField()
    etape_suivante = models.ForeignKey(
        "self", null=True, on_delete=models.CASCADE, blank=True
    )

    def __str__(self):
        return self.nom


class Stock(models.Model):
    ressource = models.ForeignKey(
        Ressource, blank=True, null=True, on_delete=models.CASCADE
    )
    nombre = models.IntegerField()
    usine = models.ForeignKey(Usine, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.ressource.nom + " : {}".format(self.nombre)

    def costs(self):
        return self.nombre * self.ressource.prix


class Produit(Objet):
    premiere_etape = models.ForeignKey(
        Etape, blank=True, null=True, on_delete=models.CASCADE
    )

    def calculAchatRessources(self):
        liste_ressources_necessaires = []
        liste_ressources_a_achete = []
        etape = self.premiere_etape
        while etape.etape_suivante is not None:
            liste_ressources_necessaires.append(etape.quantite_ressource)
        for quantite_ressource in liste_ressources_necessaires:
            if not Stock.objects.filter(ressource=quantite_ressource.ressource).exists:
                liste_ressources_a_achete.append[quantite_ressource]
            else:
                quantite_ressource.quantite = (
                    quantite_ressource.quantite
                    - Stock.objects.filter(
                        ressource=quantite_ressource.ressource
                    ).first()
                )
                if quantite_ressource.quantite > 0:
                    liste_ressources_a_achete.append[quantite_ressource]
        affichage = ""
        for quantite_ressource in liste_ressources_a_achete:
            affichage = affichage + "\n - {} {}".format(
                quantite_ressource.nom, quantite_ressource.quantite
            )
        return affichage
