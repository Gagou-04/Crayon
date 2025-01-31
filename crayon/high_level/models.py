# Create your models here.
from django.db import models


class Ville(models.Model):
    nom = models.CharField(max_length=100)
    code_postal = models.IntegerField()
    prix_m_2 = models.IntegerField()

    def __str__(self) -> str:
        return self.nom

    def json(self) -> dict:
        d = {
            "id": self.id,
            "nom": self.nom,
            "code_postal": self.code_postal,
            "prix_m_2": self.prix_m_2,
        }
        return d

    def json_extended(self) -> dict:
        return self.json()


class Local(models.Model):
    nom = models.CharField(max_length=100)
    ville = models.ForeignKey(Ville, blank=True, null=True, on_delete=models.PROTECT)
    surface = models.IntegerField()

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.nom


class SiegeSocial(Local):
    CEO = models.CharField(max_length=100)

    def json(self) -> dict:
        d = {
            "id": self.id,
            "nom": self.nom,
            "ville": self.ville.nom,
            "surface": self.surface,
            "CEO": self.CEO,
        }
        return d

    def json_extended(self) -> dict:
        return self.json()


class Machine(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.IntegerField()
    n_serie = models.IntegerField()

    def __str__(self) -> str:
        return self.nom

    def costs(self) -> float:
        return self.prix

    def json(self) -> dict:
        d = {
            "id": self.id,
            "nom": self.nom,
            "prix": self.prix,
            "n_serie": self.n_serie,
        }
        return d

    def json_extended(self) -> dict:
        return self.json()


class Usine(Local):
    machines = models.ManyToManyField(Machine)

    def costs(self) -> float:
        cout = 0
        for machine in self.machines.all():
            cout = cout + machine.costs()

        cout = cout + self.surface * self.ville.prix_m_2

        for stock in self.stock_set.all():
            cout = cout + stock.costs()

        return cout

    def json(self) -> dict:
        liste_machines = []
        for machine in self.machines.all():
            liste_machines.append(machine.nom)
        d = {
            "id": self.id,
            "nom": self.nom,
            "ville": self.ville.nom,
            "surface": self.surface,
            "machines": liste_machines,
        }
        return d

    def json_extended(self) -> dict:
        liste_machines = []
        for machine in self.machines.all():
            liste_machines.append(machine.json_extended())
        d = {
            "id": self.id,
            "nom": self.nom,
            "ville": self.ville.json_extended(),
            "surface": self.surface,
            "machines": liste_machines,
        }
        return d


class Objet(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.IntegerField()

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.nom


class Ressource(Objet):
    def __str__(self) -> str:
        return self.nom

    def json(self) -> dict:
        d = {
            "id": self.id,
            "nom": self.nom,
            "prix": self.prix,
        }
        return d

    def json_extended(self) -> dict:
        return self.json()


class QuantiteRessource(models.Model):
    ressource = models.ForeignKey(
        Ressource, blank=True, null=True, on_delete=models.CASCADE
    )
    quantite = models.IntegerField()

    def __str__(self) -> str:
        return self.ressource.nom + ": {}".format(self.quantite)

    def costs(self) -> float:
        return self.quantite * self.ressource.prix

    def json(self) -> dict:
        d = {
            "id": self.id,
            "ressource": self.ressource.nom,
            "quantite": self.quantite,
        }
        return d

    def json_extended(self) -> dict:
        d = {
            "id": self.id,
            "ressource": self.ressource.json_extended(),
            "quantite": self.quantite,
        }
        return d


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

    def __str__(self) -> str:
        return self.nom

    def json(self) -> dict:
        d = {
            "id": self.id,
            "nom": self.nom,
            "machine": self.machine.nom,
            "quantite_ressource": self.quantite_ressource.ressource.nom,
            "duree": self.duree,
            "etape_suivante": self.etape_suivante.nom,
        }
        return d

    def json_extended(self) -> dict:
        d = {
            "id": self.id,
            "nom": self.nom,
            "machine": self.machine.json(),
            "quantite_ressource": self.quantite_ressource.json_extended(),
            "duree": self.duree,
        }
        if self.etape_suivante:
            d["etape_suivante"] = self.etape_suivante.json_extended()
        else:
            d["etape_suivante"] = None
        return d


class Stock(models.Model):
    ressource = models.ForeignKey(
        Ressource, blank=True, null=True, on_delete=models.CASCADE
    )
    nombre = models.IntegerField()
    usine = models.ForeignKey(Usine, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.ressource.nom + " : {}".format(self.nombre)

    def costs(self) -> float:
        return self.nombre * self.ressource.prix

    def json(self) -> dict:
        d = {
            "id": self.id,
            "ressource": self.ressource.nom,
            "nombre": self.nombre,
            "usine": self.usine.nom,
        }
        return d

    def json_extended(self) -> dict:
        d = {
            "id": self.id,
            "ressource": self.ressource.json_extended(),
            "nombre": self.nombre,
            "usine": self.usine.json_extended(),
        }
        return d


class Produit(Objet):
    premiere_etape = models.ForeignKey(
        Etape, blank=True, null=True, on_delete=models.CASCADE
    )

    def calculAchatRessources(self) -> list:
        liste_ressources_necessaires = []
        liste_ressources_a_achete = []
        etape = self.premiere_etape
        liste_ressources_necessaires.append(etape.quantite_ressource)
        while etape.etape_suivante is not None:
            etape = etape.etape_suivante
            liste_ressources_necessaires.append(etape.quantite_ressource)
        for quantite_ressource in liste_ressources_necessaires:
            if (
                Stock.objects.filter(ressource=quantite_ressource.ressource).first()
                is None
            ):
                liste_ressources_a_achete.append(quantite_ressource)
            else:
                quantite_ressource.quantite = (
                    quantite_ressource.quantite
                    - Stock.objects.filter(ressource=quantite_ressource.ressource)
                    .first()
                    .nombre
                )
                if quantite_ressource.quantite > 0:
                    liste_ressources_a_achete.append(quantite_ressource)
        print("Ressources en stock :")
        if Stock.objects.first() is None:
            print(" Aucun stock")
        else:
            print(Stock.objects.all())
            for stock in Stock.objects.all():
                print(" - ", stock)
            print("Ressources a acheter :")
        for quantite_ressource in liste_ressources_a_achete:
            print(" - ", quantite_ressource)
        return liste_ressources_a_achete

    def json(self) -> dict:
        d = {
            "id": self.id,
            "nom": self.nom,
            "prix": self.prix,
            "premiere_etape": self.premiere_etape.nom,
        }
        return d

    def json_extended(self) -> dict:
        d = {
            "id": self.id,
            "nom": self.nom,
            "prix": self.prix,
            "premiere_etape": self.premiere_etape.json_extended(),
        }
        return d
