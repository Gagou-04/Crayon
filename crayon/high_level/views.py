# Create your views here.

from django.views.generic import DetailView
from django.http import JsonResponse
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


class VilleDetailView(DetailView):
    model = Ville

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(self.object.json(), safe=False)


class SiegeSocialDetailView(DetailView):
    model = SiegeSocial

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(self.object.json(), safe=False)


class MachineDetailView(DetailView):
    model = Machine

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(self.object.json(), safe=False)


class UsineDetailView(DetailView):
    model = Usine

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(self.object.json(), safe=False)


class RessourceDetailView(DetailView):
    model = Ressource

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(self.object.json(), safe=False)


class QuantiteRessourceDetailView(DetailView):
    model = QuantiteRessource

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(self.object.json(), safe=False)


class EtapeDetailView(DetailView):
    model = Etape

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(self.object.json(), safe=False)


class StockDetailView(DetailView):
    model = Stock

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(self.object.json(), safe=False)


class ProduitDetailView(DetailView):
    model = Produit

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(self.object.json(), safe=False)
