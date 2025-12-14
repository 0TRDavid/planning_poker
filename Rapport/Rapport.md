Comparaison biblio back end :

![alt text](image.png)

choix front : react.js

## 1. Découvrir React.js
et création de l'app planning_poker dans Django (parce que c'est les règles de l'art)

## Enregistrer un utilisateur dans un cookie (ETQU je veux m'identifier avec mon nom)


## Définir le format du json


## En tant qu'utilisateur, je veux afficher les sessions de planning poker


Création de session dans model.py
Serialization de la sortie de la table Session pour envoyer un JSON via l'API vers le front
affichage du JSON récupéré dans le Front
## Importer les userstory du json et les afficher


### ETQU je veux créé une session dans la base de donnée en important mon JSON

### ETQU je veux rejoindre une session existante 

### ETQUS on veut jouer 



Une table partie dans le back qui recois lorsque l'utilisateur rejoins la session son username, l'id_session ensuite cela est modifié quand il vote. Quand tous les utilisateur on bollean = True sur a voter pour la meme session, 
 1 . le champ stories de la table Session est modifié (on renvoi un nouveau JSON en ajoutant une valeur à la userstory!!)
 2 . les valeurs dans la table partie sont remises à False et rien pour la valeur votée 

 3 . on passe à l'affichage de la troisieme userstory
 S


 Si une session est pleine, empecher de la rejoindre ou page de dl ! par contre on ne peut le faire qu'une seule fois !! vider table partie a l'ouverture re resultat ?!  

Ajouter un bouton pour la pause cafe, ce qui revient a l'accueil en supprimant les joueurs !! la partie est save!
ajouter un nombvre de participant à la création!

Il faut :

creer les tests front
commenter auto le code
tester les modes de jeu... fait avec les tests ?
gerer la pause café! et le ? + la boucle front si strict et retour -1 de closestory!
