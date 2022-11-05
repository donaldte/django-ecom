from django.shortcuts import render
from .models import *

def shop(request, *args, **kwargs):
    """ vue principale """

    produits = Produit.objects.all()

    context = {
        'produits':produits
    }

    return render(request, 'shop/index.html', context)


def panier(request, *args, **kwargs):
    """ panier """
    
    if request.user.is_authenticated:

        client = request.user.client

        commande, created = Commande.objects.get_or_create(client=client, complete=False)

        articles = commande.commandearticle_set.all()

    else:

        articles = []   

        commande = {
            'get_panier_total':0,
            'get_panier_article':0
        }

    context = {
        'articles':articles,
        'commande':commande
    }

    return render(request, 'shop/panier.html', context)


def commande(request, *args, **kwargs):
    """ Commande """

    if request.user.is_authenticated:

        client = request.user.client

        commande, created = Commande.objects.get_or_create(client=client, complete=False)

        articles = commande.commandearticle_set.all()

    else:

        articles = []   

        commande = {
            'get_panier_total':0,
            'get_panier_article':0
        }

    context = {
        'articles':articles,
        'commande':commande
    }

    return render(request, 'shop/commande.html', context)    