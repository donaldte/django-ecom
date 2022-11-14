from django.urls import path 
from . import views

app_name = "shop"

urlpatterns = [ 
    path('', views.shop, name='shop'),

    path('panier/', views.panier, name='panier'),
    
    path('commande/', views.commande, name='commande'),

    path('update_article/', views.update_article, name='update_article'),

    path('traitement-commande/', views.traitementCommande, name="traitement_commande")
]