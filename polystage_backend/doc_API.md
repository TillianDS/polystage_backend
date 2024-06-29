
# commandes bash pour le serveur

## lancer le serveur

```json
python3 manage.py runserver
```

## mettre à jour les migrations

```json
python3 manage.py makemigrations 
python3 manage.py migrate
```

# URL

Chaque endpoint de l'API polystage Backend est détaillé ci dessous. Certaines vues sont CRUD d'autres ne le sont pas.

## organisation vues CRUD

Chaque model possède une implémentation avec des fonctions CRUD (create, read update, delete).

Cette implémentation CRUD est dedontante à chaque model, nous n'allons pas détailler le fonctionnement à chaque fois, nous préciserons pour chaque url, les informations nécessaires à envoyer et les informations reçus.

Les vues CRUD sont organisé de la manière suivante :

On a deux class ModelList et ModelDetails

### modelList

```
url : http://127.0.0.1:8000/modelList/
```

méthode :  GET, POST

#### GET

Renvoie toutes les données de la table en question

#### POST

Permet d'enregisrer dans la table une instance du model en question en fournissant dans la requête les informations nécessaires

### modelDetails

Permet d'accèder à un instance précise de la table, à la fin de l'url il faut rajouter la clé primaire (un entier : integer) de l'instance sur laquelle la requête va s'appliquer.

```
url : http://127.0.0.1:8000/modelDetail/<integer>/
```

méthode : GET, PUT, DELETE

#### GET

Renvoie les informations de l'instance spécifié

#### PUT

Permet de modifier les informations de l'instance.

#### Données à envoyer

Les données que l'ont a modifié ET AUSSI celle qui n'ont pas été modifié.

Django compare ensuite les informations et modifie celle qui ont changée.

### Données reçues

Les données de l'instance modifiée

#### DELETE

Supprimer l'instance spécifiée.

#### Données à envoyer

Aucune information de plus que la clé primaire dans l'url n'est nécessaire.

#### Données reçues

Lors de la suppression renvoie un message :

```json
{
    "success": "{{NomModelInstance}} supprimé avec succès"
}
```

#### Infos

Les données ne sont pas réellement supprimées de la base, elles prennent le statu `is_active = True` ce qui les rend non visible par toutes les requetes (à part en utilisant un autre objet du model Django)

## autres vues

Un certains nombre de vue prennent d'autres formes et seront détaillées plus en détails

# Utilisateurs

## CRUD

### URL

```url
http://127.0.0.1:8000/userList/

http://127.0.0.1:8000/userDetails/<int>/
```

### les informations de l'utilisateur

- id (int) : identfifiant de l'utilisateur
- email (email) : email de l'utilisateur
- first_name (string) : prenom
- last_name (string) : prenom
- first_connection (boolean): est ce la première connection de l'utilisateur ? true si premiere connection, false s'il s'est déjà connecté
- profile (string: profile) : profile de l'utilisateur

#### les profiles possibles pour un utilisateur

- ENS : enseignant
- ADM : admin
- ETU : etudiant
- TUT : tuteur
- PRO : professionnel

### pour les etudiants on trouve en plus

- num_etudiant (int) : numéro de l'etudiant

##### Données à envoyer

- email (email) : email du user
- first_name (string) : prenom
- last_name (string) : prenom
- profile (profile) : profile de l'utilisateur

pour les etudiants on trouve en plus :

- idFiliere :
- num_etudiant (int) : numéro de l'etudiant

##### Données reçues

informations de l'utilisateur crée

```json
http://127.0.0.1:8000/userList/ENS/
{
        "id": 12,
        "email": "enseignant5@po.fr",
        "first_name": "Benoit",
        "last_name": "Favre",
        "first_connection": True,
        "profile": "ENS"
    }
```

# Filiere

## CRUD

### URL

```url
http://127.0.0.1:8000/filiereList/

http://127.0.0.1:8000/userDetails/<int>/
```

### informations d'une filiere

- id (int) : id de la filiere
- nom (string)  : nom filiere

```json

{
    "id": 2,
    "nom": "Genie Biologique",
}
```

# Promo

## Informations d'une promo

- id (int): id de la promo
- annee (int) : annee de la promo
- filiere (int) : id de la filiere à laquelle appartient la promo

```json
{
    "id": 4,
    "annee": 2027,
    "filiere": 2
}
```

## CRUD

### URL

```url
http://127.0.0.1:8000/promoList/

http://127.0.0.1:8000/promoDetails/<int>/
```

# PromoFiliere

vues liées à la prom oet à la filière en même temps

## promoFiliere

méthode : GET

```url
http://127.0.0.1:8000/promoFiliere/
```

affiche toutes les promos avec la filiere associé

### Données reçues

```json
[
    {
        "id": 2,
        "annee": 2026,
        "filiere": {
            "id": 2,
            "nom": "Genie Biologique"
        }
    },
    {
        "id": 4,
        "annee": 2027,
        "filiere": {
            "id": 2,
            "nom": "Genie Biologique"
        }
    }
]
```

## getPromoOfFiliere

renvoie les promos d'une filiere

méthode : POST

```url
getPromoOfFiliere/
```

### Données à envoyer

```json
{
    "id_filiere" :  "id de la filiere"
}
```

### Données reçues

toutes les promos associées

```json
[
    {
        "id": 4,
        "annee": 2027,
        "filiere": 2
    },
    {
        "id": 5,
        "annee": 2028,
        "filiere": 2
    },
    {
        "id": 6,
        "annee": 2029,
        "filiere": 2
    }
]
```

# Stage

## informations d'un stage

- id (int) : id du stage
- sujet (string)  : sujet du stage
- nom_entreprise (string): nom de l'entreprise dans lequel se déroule le stage
- Confidentiel (booléen) : le stage est il Confidentiel ?
- date_debut (date) : date de debut de stage
- date_fin (date) : date de fin de stage
- tuteur (int) : id du tuteur

```json
{
    "id": 2,
    "confidentiel": true,
    "sujet": "Gestion des cellules",
    "date_debut": "2024-01-18",
    "date_fin": "2024-08-18",
    "nom_entreprise": "Biomérieux",
    "tuteur": 3
}
```

## CRUD

### url

```url
http://127.0.0.1:8000/stageList/

http://127.0.0.1:8000/stageDetails/<int>/
```

# Soutenance

## CRUD

### URL

```url
http://127.0.0.1:8000/soutenanceList/

http://127.0.0.1:8000/soutenanceDetails/<int>/
```

### Informations d'une soutenance

- id : id de la soutenance
- etudiant: id de l'étudiant
- jury: id du jury
- stage: id du stage
- date_soutenance: date du déroulement de la soutenance
- heure_soutenance: heure du déroulement de la soutenance
- note: note de la soutenance

```json
{
    "id" : 1,
    "etudiant": 32,
    "jury": 1,
    "stage": 2,
    "date_soutenance": "03-09-2024",
    "heure_soutenance": "11:50",
    "note": 15.0
}
```

## setNote

permet au jury de définir la note
la note doit être comprise entre 0 et 20, elle peut être décimal, au format 18.5 ou 18,5.

Pour modifier la note l'utilisateur doit être leader du jury

### URL

Méthode : POST

```url
http://127.0.0.1:8000/setNote/
```

### informations envoyées

```json
{
    "id_user" : "id de l'utilisateur",
    "id_soutenance" : "soutenance à laquelle on veut définir la note",
    "id_jury" : "id du jury",
    "note" : "la note à définir"
}
```

### informations reçues

#### sucess

```json
{
    {"success":"la note a bien été enregistré"}
}
```

#### non success

- si la note n'est pas comprise entre 0 et 20

- si l'utilisateur n'est pas leader du jury

- si la note n'est pas dans le bon format

```json
{
    "errors":"cause de l'erreur"
}
```


## getJurySoutenance

permet d'obtenir les soutenances et étudiants, associés au jury

### URL

Méthode : POST

```url
http://127.0.0.1:8000/getJurySoutenance/
```

### informations envoyées

```json
{
    "id_jury" : "id du jury",
}
```

### informations reçues

#### sucess

```json
[
    {
        "id": 3,
        "date_soutenance": "30-06-2024",
        "heure_soutenance": "11:00",
        "etudiant": {
            "id": 50,
            "email": "etu1@po.fr",
            "first_name": "etu1",
            "last_name": "etu1",
            "first_connection": false,
            "profile": "ETU",
            "num_etudiant": "d00001",
            "promo": 7
        },
        "is_active": true,
        "note": 20.0,
        "jury": 8
    },
    {
        "id": 4,
        "date_soutenance": "30-06-2024",
        "heure_soutenance": "12:00",
        "etudiant": {
            "id": 51,
            "email": "etu2@po.fr",
            "first_name": "etu2",
            "last_name": "etu2",
            "first_connection": false,
            "profile": "ETU",
            "num_etudiant": "d00002",
            "promo": 7
        },
        "is_active": true,
        "note": null,
        "jury": 8
    }
]
```

#### non success

- le jury n'existe pas

```json
{
    "errors":"cause de l'erreur"
}
``

# Jury

## Informations d'un Jury

```json
```

## CRUD

### URL

```url
http://127.0.0.1:8000/juryList/

http://127.0.0.1:8000/juryDetails/<int>/
```

## isJury

obtenir l'information si l'utilisateur passé en paramètre est un jury 

### URL

Méthode : POST

```url
http://127.0.0.1:8000/isJury/
```

### informations envoyées

```json
{
    "id_user" : "id de l'utilisateur"
}
```

### informations reçues

#### sucess

```json
{
    "is_jury": true,
    "jury": [ //les jurys auxquels appartient l'utilisateur
        8 
    ]
}
```

#### non success

```json
{
    "is_jury": false,
    "jury": []
}
```

## becomeLeader

definie un user comme leader d'un jury

### URL

Méthode : POST

```url
http://127.0.0.1:8000/becomeLeader/
```

### informations envoyées

```json
{
    "id_user" : "id de l'utilisateur",
    "id_jury" : "id du jury dont on veut le mettre leader"
}
```

### informations reçues

#### sucess

```json
{
    "success": "changement du leader du jury",
    "leader": 54 //id du membre du jury

}
```

#### non success

- si l'utilisateur n'est pas un membre de jury

- si l'utilisateur ne fait pas partie du jury spécifié

```json
{
    {"errors":"cause de l'erreur"}
}
```

# Authentification

### login

permet d'authentifier l'utilisateur et de la connecter à l'application

```url
http://127.0.0.1:8000/login/
```

#### POST

##### arguments requete

- "email" : email de l'utilisateur
- "password" : mot de passe

##### response

si les identifiants sont correctes:

- "id" : identifiants utilisateurs
- "token" : token d'authentification
- "type utilisateur" : type de l'utilisateur qui se connecte

```json
{
    "token": "a5d8e22e748f34af4205d2b2714b22a4a7bcdcbe",
    "user_id": 14,
    "profile": "ADM"
}
```

##### response

- success : message de succès

## utilisateur avec toutes les infos stage, promo, filiere et soutenance

```url
http://127.0.0.1:8000/etudiantAll/<int:idEtudiant>/
```

###  envoie

on passe l'id de l'utilisateur dans l'url

### retour

renvoie les informations de l'utilisateur avec son stage, sa promo, sa filière et sa soutenance

```json
{
    "id": 34,
    "email": "tiit@po.fr",
    "first_name": "tillian",
    "last_name": "dhume",
    "first_connection": false,
    "profile": "ETU",
    "num_etudiant": "d2201421",
    "promo": {
        "id": 4,
        "annee": 2027,
        "filiere": {
            "id": 2,
            "nom": "Genie Biologique"
        }
    },
    "stage": [
        {
            "id": 2,
            "tuteur": {
                "id": 30,
                "email": "tuteur2@po.fr",
                "first_name": "tuteur",
                "last_name": "tuteur",
                "first_connection": false,
                "profile": "TUT"
            },
            "sujet": "Optimisation des cultures de bactéries",
            "confidentiel": false,
            "date_debut": "2024-01-10",
            "date_fin": "2024-08-18",
            "nom_entreprise": "Biomérieux"
        }
    ]
}
```

# export

## exportNote

méthode : POST

```url
http://127.0.0.1:8000/exportNote/
```

### envoie

- filiere (string) : nom de la filiere
- annee (int) : année de la promo

### retourne

```json
[
    {
        "num_etudiant": "d22014217",
        "first_name": "Tillian",
        "last_name": "Dhume",
        "promo_annee": 2027,
        "filiere": "Genie Biologique",
        "note_soutenance": null
    },
    {
        "num_etudiant": "d2201421",
        "first_name": "tillian",
        "last_name": "dhume",
        "promo_annee": 2027,
        "filiere": "Genie Biologique",
        "note_soutenance": 15.0
    },
    {
        "num_etudiant": "d2201421",
        "first_name": "tillian",
        "last_name": "dhume",
        "promo_annee": 2027,
        "filiere": "Genie Biologique",
        "note_soutenance": 15.0
    },
    {
        "num_etudiant": "d22014217",
        "first_name": "tillian",
        "last_name": "dhume",
        "promo_annee": 2027,
        "filiere": "Genie Biologique",
        "note_soutenance": null
    }
]
```

# Gestion des formulaires

le formulaire est composé de plusieurs tables, Formulaire, Question, Checkbox et Reponse

Un formulaire peut avoir plusieurs questions, si la question est de type checkbox elle peut avoir plusieurs éléments checkbox, les réponses sont associès à chaque question ainsi qu'à un utilisateur
# Formulaire

## Informations d'un formulaire

## CRUD


## Response

### Informations d'un réponse

- id (string) : id de la response
- content (string): contenu de la response
- question (int) : id de la question associée
- user (int) : id de l'utilisateur

```json

{
    "id": 2,
    "content": "oui",
    "question": 4,
    "user": 33
}
```

### CRUD

#### URL

```url
http://127.0.0.1:8000/responseList/
http://127.0.0.1:8000/responseDetails/<int>/
```

## ResponseFormulaire

renvoie le formulaire, les questions et checkbox associés en fonction de l'étudiant concerné

### URL

```url
http://127.0.0.1:8000/responseFormulaire/
```

### Données envoyées

```json
{
    "etudiant_id" : "id de l'étudiant associé",
    "id_formulaire" : "id du formulaire souhaité"
}
```

# Autres endpoints formulaire

## getFormulaireAll

getFormulaireAll permet de récupérer l'ensemble des informations d'un formulaire : l'entité formulaire avec les questions et les checkbox 

### URL

methode : GET

```url
http://127.0.0.1:8000/getFormulaireAll/<str:pk>/
```

pk : la clé primaire du formulaire

#### données reçues

les informations de toutes le formulaire

```json
[
    {
        "id": "id",
        "title": "Avis du tuteur",
        "description": "formulaire pour l'evaluation de Louise",
        "question": [
            {
                "id": 4,
                "title": "qu'avez vous pensé du stagiaire ?",
                "type": "text",
                "checkbox": []
            },
            {
                "id": 6,
                "title": "qu'avez vous pensé du stagiaire ?",
                "type": "checkbox",
                "checkbox": [
                    {
                        "id": 1,
                        "title": "Oui"
                    },
                    {
                        "id": 2,
                        "title": "non"
                    }
                ]
            },
            {
                "id": 7,
                "title": "qu'avez vous pensé du stagiaire ?",
                "type": "text",
                "checkbox": []
            },
            {
                "id": 8,
                "title": "qu'avez vous pensé du stagiaire ?",
                "type": "text",
                "checkbox": []
            },
            {
                "id": 9,
                "title": "qu'avez vous pensé du stagiaire ?",
                "type": "text",
                "checkbox": []
            }
        ]
    }
]
```

## createFormulaireAll

enregistrement de toute l'architecture d'un formulaire d'un seul coup ; formulaire, question, checkbox

### URL

methode : POST

```url
http://127.0.0.1:8000/createFormulaireAll/
```

### données envoyées

```json
{
    "id": "materiau",
    "question": [
        {
            "id": 10,
            "titre": "qu'avez vous fati durantvotre stage",
            "type": "checkbox",
            "checkbox": []
        },
        {
            "id": 11,
            "titre": "le stage vous a t'il plue?",
            "type": "checkbox",
            "checkbox": [{
                        "id": 1,
                        "title": "Oui"
                    },
                    {
                        "id": 2,
                        "title": "non"
                    }]
        }
    ],
    "titre": "avis sur le stage",
    "description": "avis de l'étudiant sur le déroulement de son stage",
    "profile": "ETU",
    "langue": "FR",
    "filiere": 6
}
```


## retrieveFormulaire

retrouve un formulaire

### URL

methode : POST

```url
http://127.0.0.1:8000/retrieveFormulaire/
```

### données envoyées

```json
{
    "id": "materiau",
    "question": [
        {
            "id": 10,
            "titre": "qu'avez vous fati durantvotre stage",
            "type": "checkbox",
            "checkbox": []
        },
        {
            "id": 11,
            "titre": "le stage vous a t'il plue?",
            "type": "checkbox",
            "checkbox": [{
                        "id": 1,
                        "title": "Oui"
                    },
                    {
                        "id": 2,
                        "title": "non"
                    }]
        }
    ],
    "titre": "avis sur le stage",
    "description": "avis de l'étudiant sur le déroulement de son stage",
    "profile": "ETU",
    "langue": "FR",
    "filiere": 6
}
```

# Import des données

## Fonctionnement

Permet d'importer des données massivement, sous format JSON. Si l'instance importé existe déjà dans la base cela modifie ses informations par rapport à celle envoyées. Si l'instance est inactive, cela la rend active.

### Données envoyées

l'envoie des données se fait sous format JSON, un tableau contient chaque champ de l'instance à créer

```json
[
    //instance 1
    {
        "clé" : "valeur",
        "clé" : "valeur"

    },
    //instance 2
    {
        "clé" : "valeur",
        "clé" : "valeur"
    },

    //...
]
```

### Données reçues

si certaines données n'ont pas pu être importée à cause d'erreurs cela renvoie l'instance en question avec la cause de l'error, les données en erreurs ne sont pas importés, celles qui n'ont pas d'erreurs sont importées. Si il n'y aucune erreur, cela renvoie un message de succés

#### Sucess

```json
{
    "success": "tous les {models} ont été crées avec succès"
}
```

#### Errors

```json
{
    "errors": [
        {
            "nomInstance": {
                //instance
            },
            "errors": {
                //erreur rencontré lors de l'enregistrement
            }
        },
        {
            "nomInstance": {
                //instance
            },
            "errors": {
                //erreur rencontré lors de l'enregistrement
            }
        },
        {
            "nomInstance": {
                //instance
            },
            "errors": {
                //erreur rencontré lors de l'enregistrement
            }
        }
    ]
}
```

## Import des utilisateurs

permet d'import des utilisateurs en masse.

### URL

méthode : POST

```url
http://127.0.0.1:8000/importUser/
```

### Données à envoyer

données des

```json
[
    {
        "email": "test@po.fr",
        "first_name": "",
        "last_name": "jean",
        "profile": "TUT"
    },
    {
        "email": "enseignant10@po.fr",
        "first_name": "Benoit",
        "last_name": "Favre",
        "profile": "ENS"
    },
    {
        "email": "titi@po.fr",
        "first_name": "Titi",
        "last_name": "Titi",
        "profile": "ETU",
        "promo" : 5,
        "num_etudiant" : "d22014217"
    }
]
```

### Données reçues

```json

```

## Import des Stages

### URL

méthode : POST

```url
http://127.0.0.1:8000/importStage/
```

### Données à envoyer

```json
[
    {
        "email_tuteur": "tim-ross@amu.fr",
        "sujet": "Gestion du Run",
        "confidentiel": false,
        "date_debut": "2024-06-03",
        "date_fin": "2024-08-2",
        "nom_entreprise": "April",
        "num_etudiant": "d030232"
    }
]
```

### Données reçues

```json
```

## Import des Soutenances

```url
http://127.0.0.1:8000/importSoutenance/
```

### Données à envoyer

```json
```

### Données reçues

```json
```

## Import des Jurys

```url
importJury/
```

### Données à envoyer

```json
```

### Données reçues

```json
```

# Search

rechercher dans les différentes tables selon un / des critères souhaité

## userSearch

recherche un utilisateur selon son nom, prénom, email ou numéro étudiant (si étudiant). Le champ n'a pas besoin d'être entier, on regarde dans chaque colonne pour chaque utilisaterur si un champ contient la propriété recherché.

```url
userSearch/
```

### Données à envoyer

```json
{
    "search" :  "champ à chercher"
}
```

### Données reçues

```json
envoie : 
{
    "search" :  "jea"
}

reçus :
    [
        {
            "id": 34,
            "email": "jean@po.fr",
            "first_name": "tillian",
            "last_name": "dhume",
            "first_connection": false,
            "profile": "ETU",
            "num_etudiant": "d2201421",
            "promo": 4
        },
        {
            "id": 6,
            "email": "enseignant@po.fr",
            "first_name": "jean",
            "last_name": "jean",
            "first_connection": false,
            "profile": "ENS"
        },
        {
            "id": 35,
            "email": "test@po.fr",
            "first_name": "",
            "last_name": "jean",
            "first_connection": true,
            "profile": "TUT"
        },
    ]
```

## stageSearch

recherche un stage

la recherche se fait sur le sujet, le nom de l'entreprise, le numéro étudiant

```url
stageSearch/
```

### Données à envoyer

```json
{
    "search" :  "champ à chercher"
}
```

### Données reçues

les stages correspondants

```json
```

## soutenanceSearch

recherche un stage

```url
soutenanceSearch/
```

### Données à envoyer

```json
{
    "search" :  "champ à chercher"
}
```

### Données reçues

```json
```

## formulaireSearch

permet de rechercher un formulaire selon son titre, sa description, le rôle à qui il s'adresse, sa filière

```url
http://127.0.0.1:8000/formulaireSearch/
```

### Données à envoyer

```json
{
    "search" :  "champ à chercher"
}
```

### Données reçues

```json
envoie : 
{
    "search" :  "form"
}

reçus :
    [
        {
            "id": "id",
            "titre": "Avis du tuteur",
            "description": "formulaire pour l'evaluation de Louise",
            "profile": "ETU",
            "langue": "FR",
            "filiere": 5
        },
        {
            "id": "formulaire",
            "titre": "soutenance de stage",
            "description": "evaluation du jury",
            "profile": "ETU",
            "langue": "FR",
            "filiere": 5
     },
    ]

```

# Autres

### codeReset

envoie un mail à l'utilisateur avec son code de réinitilisation, s'il existe
si l'utilisateur n'existe pas, on a le même message de succès mais aucun mail n'est envoyé

```url
http://127.0.0.1:8000/codeReset/
```

#### POST

##### arguments requete

- "email" : email de l'utilisateur

##### response

```json
{
    "success": "email envoyé avec succès"
}
```

### change password

permet de changer modifier le mot de passe d'un utilisateur
le mot de passe doit contenir une majuscule, une minuscule, un caractère spécial et doit avoir une taille minimum de 7 caractères

```url
http://127.0.0.1:8000/password/
```

#### POST

##### arguments requete

- "email" : email de l'utilisateur dont on souhaite modifier le mdp
- password1 (string) : mdp de l'utilisateur
- password2 (string) : confirmation du mdp de l'utilisateur

les mdp doivent contenir une majuscule, une minuscule, un caractère spécial parmis [()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?] et doivent avoir uen longueur d'au moins 7 caractères

##### response

informations de l'utilisateur

```json
    {
        "id": 21,
        "email": "enseignant14@po.fr",
        "first_name": "Benoit",
        "last_name": "Favre",
        "first_connection": true,
        "profile": "ENS"
    }
```
