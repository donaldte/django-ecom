var produitBtns = document.getElementsByClassName('update-panier');

for (var i = 0; i < produitBtns.length; i++){

    produitBtns[i].addEventListener('click', function(){

        var produitId = this.dataset.produit;

        var action = this.dataset.action;

        if (user === "AnonymousUser"){
            addCookieArticle(produitId, action);
        }else{
            updateUserCommande(produitId, action);
        }
    })

}


function addCookieArticle(produitId, action){
    console.log("l'utilisateur n'est pas authentifie");

    if(action == "add"){
        if(panier[produitId] == undefined){
            panier[produitId] = {"qte":1};
        }else{
            panier[produitId]["qte"] += 1;
        }
    }

    if(action == "remove"){
        panier[produitId]["qte"] -= 1;
        if( panier[produitId]["qte"] <= 0){
            delete panier[produitId];
        }
    }


    document.cookie = "panier=" + JSON.stringify(panier) + ";domain=;path=/";

    console.log(panier);
    location.reload();
}

function updateUserCommande(produitId, action){

    var url = '/update_article/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({"produit_id": produitId, "action": action})
    })

    .then((response) => {
        return response.json();
    })

    .then((data) => {
        console.log('data', data);
        location.reload();
    })
}