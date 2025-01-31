# Create your tests here.
from django.test import TestCase
from .models import (
    Ville,
    SiegeSocial,
    Machine,
    Usine,
    Ressource,
    QuantiteRessource,
    Etape,
    Stock,
    Produit,
)


class VilleModeTests(TestCase):
    def test_ville_creation(self):
        self.assertEqual(Ville.objects.count(), 0)
        Ville.objects.create(nom="Toulouse", code_postal=31000, prix_m_2=10000)
        self.assertEqual(Ville.objects.count(), 1)


class SiegeSocialModeTests(TestCase):
    def test_siegeSocial_creation(self):
        self.assertEqual(SiegeSocial.objects.count(), 0)
        Ville.objects.create(nom="Toulouse", code_postal=31000, prix_m_2=10000)
        SiegeSocial.objects.create(
            nom="QG", ville=Ville.objects.first(), surface=1000, CEO="DURAND"
        )
        self.assertEqual(SiegeSocial.objects.count(), 1)
        self.assertEqual(SiegeSocial.objects.first().ville.nom, "Toulouse")


class MachineModeTests(TestCase):
    def test_machine_creation(self):
        self.assertEqual(Machine.objects.count(), 0)
        Machine.objects.create(nom="Scie", prix=1000, n_serie=45689)
        self.assertEqual(Machine.objects.count(), 1)


class UsineModeTests(TestCase):
    def test_usine_creation(self):
        self.assertEqual(Usine.objects.count(), 0)
        Ville.objects.create(nom="Toulouse", code_postal=31500, prix_m_2=10000)
        scie = Machine.objects.create(nom="Scie", prix=1000, n_serie=45689)
        perforeur = Machine.objects.create(nom="Perforeur", prix=2000, n_serie=69458)
        usine = Usine.objects.create(
            nom="TLS-01", ville=Ville.objects.first(), surface=5000
        )
        usine.machines.set([scie, perforeur])
        self.assertEqual(Usine.objects.count(), 1)
        self.assertEqual(Usine.objects.first().ville.code_postal, 31500)
        self.assertEqual(Usine.objects.first().machines.first().nom, "Scie")

    def test_calculCouts(self):
        Ville.objects.create(nom="Labege", code_postal=31700, prix_m_2=2000)
        scie = Machine.objects.create(nom="Scie", prix=1000, n_serie=45689)
        perforeur = Machine.objects.create(nom="Perforeur", prix=2000, n_serie=69458)
        usine = Usine.objects.create(
            nom="LAB-01", ville=Ville.objects.first(), surface=50
        )
        usine.machines.set([scie, perforeur])
        r1 = Ressource.objects.create(nom="Bois", prix=10)
        r2 = Ressource.objects.create(nom="Mine", prix=15)
        Stock.objects.create(ressource=r1, nombre=1000, usine=usine)
        Stock.objects.create(ressource=r2, nombre=50, usine=usine)
        self.assertEqual(usine.costs(), 113750)


class RessourceModeTests(TestCase):
    def test_ressource_creation(self):
        self.assertEqual(Ressource.objects.count(), 0)
        Ressource.objects.create(nom="Bois", prix=2)
        self.assertEqual(Ressource.objects.count(), 1)


class QuantiteRessourceModeTests(TestCase):
    def test_quantiteRessource_creation(self):
        self.assertEqual(QuantiteRessource.objects.count(), 0)
        Ressource.objects.create(nom="Bois", prix=2)
        QuantiteRessource.objects.create(
            ressource=Ressource.objects.first(), quantite=70
        )
        self.assertEqual(QuantiteRessource.objects.count(), 1)


class EtapeModeTests(TestCase):
    def test_etape_creation(self):
        self.assertEqual(Etape.objects.count(), 0)
        m1 = Machine.objects.create(nom="Scie", prix=1000, n_serie=45689)
        m2 = Machine.objects.create(nom="Perforeur", prix=2000, n_serie=68689)
        r1 = Ressource.objects.create(nom="Bois", prix=2)
        r2 = Ressource.objects.create(nom="Mine", prix=3)
        q1 = QuantiteRessource.objects.create(ressource=r1, quantite=70)
        q2 = QuantiteRessource.objects.create(ressource=r2, quantite=50)
        e2 = Etape.objects.create(
            nom="Inserer mine",
            machine=m2,
            quantite_ressource=q2,
            duree=5,
            etape_suivante=None,
        )
        self.assertEqual(Etape.objects.count(), 1)
        Etape.objects.create(
            nom="Perforer bois",
            machine=m1,
            quantite_ressource=q1,
            duree=15,
            etape_suivante=e2,
        )
        self.assertEqual(Etape.objects.count(), 2)


class ProduitModeTests(TestCase):
    def test_produit_creation(self):
        self.assertEqual(Produit.objects.count(), 0)
        m1 = Machine.objects.create(nom="Scie", prix=1000, n_serie=45689)
        m2 = Machine.objects.create(nom="Perforeur", prix=2000, n_serie=68689)
        r1 = Ressource.objects.create(nom="Bois", prix=2)
        r2 = Ressource.objects.create(nom="Mine", prix=3)
        q1 = QuantiteRessource.objects.create(ressource=r1, quantite=70)
        q2 = QuantiteRessource.objects.create(ressource=r2, quantite=50)
        e2 = Etape.objects.create(
            nom="Inserer mine",
            machine=m2,
            quantite_ressource=q2,
            duree=5,
            etape_suivante=None,
        )
        e1 = Etape.objects.create(
            nom="Perforer bois",
            machine=m1,
            quantite_ressource=q1,
            duree=15,
            etape_suivante=e2,
        )
        Produit.objects.create(nom="Crayon", prix=10, premiere_etape=e1)
        self.assertEqual(Produit.objects.count(), 1)

    def test_calculAchatRessources(self):
        m1 = Machine.objects.create(nom="Scie", prix=1000, n_serie=45689)
        m2 = Machine.objects.create(nom="Perforeur", prix=2000, n_serie=68689)
        r1 = Ressource.objects.create(nom="Bois", prix=2)
        r2 = Ressource.objects.create(nom="Mine", prix=3)
        q1 = QuantiteRessource.objects.create(ressource=r1, quantite=70)
        q2 = QuantiteRessource.objects.create(ressource=r2, quantite=50)
        e2 = Etape.objects.create(
            nom="Inserer mine",
            machine=m2,
            quantite_ressource=q2,
            duree=5,
            etape_suivante=None,
        )
        e1 = Etape.objects.create(
            nom="Perforer bois",
            machine=m1,
            quantite_ressource=q1,
            duree=15,
            etape_suivante=e2,
        )
        Ville.objects.create(nom="Labege", code_postal=31700, prix_m_2=2000)
        usine = Usine.objects.create(
            nom="LAB-01", ville=Ville.objects.first(), surface=50
        )
        usine.machines.set([m1, m2])
        Stock.objects.create(ressource=r1, nombre=50, usine=usine)
        Stock.objects.create(ressource=r2, nombre=40, usine=usine)
        p = Produit.objects.create(nom="Crayon", prix=10, premiere_etape=e1)
        q1_res = QuantiteRessource.objects.create(ressource=r1, quantite=20)
        q2_res = QuantiteRessource.objects.create(ressource=r2, quantite=10)
        self.assertEqual(p.calculAchatRessources(), [q1_res, q2_res])
