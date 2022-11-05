from django.db import models

from django.contrib.auth.models import User 

from django.utils import timezone


class Client(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=200, null=True)

    def __str__(self):
        return self.name 

class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
class Produit(models.Model):
    categorie = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=100, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    date_ajout = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_ajout']

    def __str__(self):
        return self.name 

    @property
    def imageUrl(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url             


class Commande(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, blank=True, null=True)
    date_commande = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True) 

    def __str__(self):
        return str(self.id)  

    @property 
    def get_panier_total(self):
        articlecommande = self.commandearticle_set.all()
        total = sum([article.get_total for article in articlecommande])
        return total  

    @property
    def get_panier_article(self):
        articlecommande = self.commandearticle_set.all()
        quantite_total = sum([article.quantite for article in articlecommande])
        return quantite_total



class CommandeArticle(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.SET_NULL, blank=True, null=True)
    commande = models.ForeignKey(Commande, on_delete=models.SET_NULL, blank=True, null=True)
    quantite = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.quantite * self.produit.price
        return total


class AddressChipping(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, blank=True, null=True)
    commande = models.ForeignKey(Commande, on_delete=models.SET_NULL, blank=True, null=True)
    addresse = models.CharField(max_length=100, null=True)
    ville = models.CharField(max_length=100, null=True)
    zipcode = models.CharField(max_length=100, null=True)
    date_ajout =  models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.addresse


    
