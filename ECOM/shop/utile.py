from . models import * 
import json


def panier_cookie(request):
    try: 
        panier = json.loads(request.COOKIES.get('panier'))
    except:
        panier = {}    

    articles = []

    commande = {
        'get_panier_total':0,
        'get_panier_article':0,
        'produit_physique':False,
    }

    nombre_article = commande['get_panier_article']
    try:

        for obj in panier:
            nombre_article += panier[obj]['qte']

            produit = Produit.objects.get(id=obj)

            total = (produit.price * panier[obj]['qte'])

            commande['get_panier_article'] += panier[obj]['qte']

            commande['get_panier_total'] += total

            article = {
                'produit':{
                    'id': produit.id,
                    'name': produit.name,
                    'price': produit.price,
                    'imageUrl': produit.imageUrl
                },

                'quantite': panier[obj]['qte'],
                'get_total': total
            }

            articles.append(article)

            if produit.digital == False:
                commande['produit_physique'] = True
                
    except:
        pass 

    context = {
        'articles': articles,
        'commande': commande,
        'nombre_article': nombre_article
    }           

    return context


def data_cookie(request):

    if request.user.is_authenticated:

        client = request.user.client

        commande, created = Commande.objects.get_or_create(client=client, complete=False)

        articles = commande.commandearticle_set.all()

   
        nombre_article = commande.get_panier_article

    else:
        
        cookie_panier = panier_cookie(request)
        articles = cookie_panier['articles']
        commande = cookie_panier['commande']
        nombre_article = cookie_panier['nombre_article']

    context = {
        'articles': articles,
        'commande': commande,
        'nombre_article': nombre_article
    }

    return context


def commandeAnonyme(request, data):
    print("utilisateur non authentifie")

    print('cookies', request.COOKIES)
    
    name = data['form']['name']
    print('data', data)
    print('name', name)
    username = data['form']['username']
    email = data['form']['email']
    phone = data['form']['phone']

    cookie_panier = panier_cookie(request)
    articles = cookie_panier['articles']

    client, created = Client.objects.get_or_create(
        email = email
    )
    
    client.name = name
    client.save()


    commande = Commande.objects.create(
        client=client
    )

    for article in articles:
        produit = Produit.objects.get(id=article['produit']['id'])

        CommandeArticle.objects.create(
            produit=produit,
            commande = commande,
            quantite = article['quantite']
        )

    return client, commande