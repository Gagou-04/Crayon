"""
URL configuration for crayon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from high_level import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ville/<int:pk>/", views.VilleDetailView.as_view(), name="ville"),
    path(
        "siege_social/<int:pk>/",
        views.SiegeSocialDetailView.as_view(),
        name="siege_social",
    ),
    path("machine/<int:pk>/", views.MachineDetailView.as_view(), name="machine"),
    path("usine/<int:pk>/", views.UsineDetailView.as_view(), name="usine"),
    path("ressource/<int:pk>/", views.RessourceDetailView.as_view(), name="ressource"),
    path(
        "quantite_ressource/<int:pk>/",
        views.QuantiteRessourceDetailView.as_view(),
        name="quantite_ressource",
    ),
    path("etape/<int:pk>/", views.EtapeDetailView.as_view(), name="etape"),
    path("stock/<int:pk>/", views.StockDetailView.as_view(), name="stock"),
    path("produit/<int:pk>/", views.ProduitDetailView.as_view(), name="produit"),
]
