
# Methode bash pour le serveur

## lancer le serveur

```bash
python3 manage.py runserver
```

## mettre à jour les migrations

```bash
python3 manage.py makemigrations 
python3 manage.py migrate
```

# URL

### Utilisateur

##### les informations de l'utilisateur :

- id (int) : identfifiant de l'utilisateur
- email (email) : email de l'utilisateur
- first_name (string) : prenom
- last_name (string) : prenom
- first_connection (boolean): est ce la première connection de l'utilisateur ? (true si premiere connection, false s'il s'est déjà connecté)
- profile (string: profile) : profile de l'utilisateur

pour les etudiants on trouve en plus :

- num_etudiant (int) : numéro de l'etudiant
- date_naissance (date) : date de naissance de l'etudiant

##### les profiles possibles pour un utilisateur

- ENS : enseignant
- ADM : admin
- ETU : etudiant
- TUT : tuteur
- PRO : professionnel

### login

permet d'authentifier l'utilisateur et de la connecter à l'application

```url
http://127.0.0.1:8000/login/
```

#### POST

##### arguments requete

- "email" : email de l'utilisateur
- "password" : nouveau mot de passe

##### response

si les identifiants :

- "id" : identifiants utilisateurs
- "token" : token d'authentification
- "type utilisateur" : type de l'utilisateur qui se connecte

```bash
{
    "token": "a5d8e22e748f34af4205d2b2714b22a4a7bcdcbe",
    "user_id": 14,
    "profile": "ADM"
}
```

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

```bash
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

```bash
    {
        "id": 21,
        "email": "enseignant14@po.fr",
        "first_name": "Benoit",
        "last_name": "Favre",
        "first_connection": true,
        "profile": "ENS"
    }
```
### UserList

afficher ou créer des utilisateurs

```url
http://127.0.0.1:8000/userList/'
```

#### POST
creation d'un user selon le profile spécifié

##### requete

- email (email) : email du user
- first_name (string) : prenom
- last_name (string) : prenom
- password1 (string) : mdp de l'utilisateur
- password2 (string) : confirmation du mdp de l'utilisateur
- profile (profile) : profile de l'utilisateur

les mdp doivent contenir une majuscule, une minuscule, un caractère spécial parmis [()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?] et doivent avoir uen longueur d'au moins 7 caractères

pour les etudiants on trouve en plus :

- idFiliere : 
- num_etudiant (int) : numéro de l'etudiant
- date_naissance (date) : date de naissance de l'etudiant

##### response

informations de l'utilisateur crée

```bash
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

### userDetails

permet d'accèder à un user spécifique, de le modifier ou de le supprimer

```url
http://127.0.0.1:8000/userDetails/<int:pk>/'
```

##### argument url

- pk (int) : id du user que l'on voudra modifier

#### GET

##### response

informations de l'utilisateur

```bash
http://127.0.0.1:8000/userDetails/1/
{
    "id": 12,
    "email": "enseignant5@po.fr",
    "first_name": "Benoit",
    "last_name": "Favre",
    "first_connection": false,
    "profile": "profile"
}
```

#### PUT

##### arguments requete

les informations que l'on veut modifier mais aussi celles qui ne changent pas

- email (email): email user
- first_name : prenom
- last_name : nom

si etudiant :

- date_naissance (string : Day-Month-Year) : date naissance
- num_etudiant (string) : numéro etudiant

##### response

```bash
http://127.0.0.1:8000/userDetails/1/
{
    "id": 25,
    "email": "BenoiFavre@po.fr",
    "first_name": "Benoit",
    "last_name": "Favre",
    "first_connection": false,
    "profile": "ENS"
}
```

#### DELETE

suprime la filiere

```bash
{
    "success": "utilisateur supprimé avec succès"
}
```

##### response

- success : message de succès

## Admin

méthode de l'admin pour la gestion des utilisateur

```url
http://127.0.0.1:8000/userSearch/
```

#### POST

##### requete

champ sur lesquels on souhaite faire la recherche

- first_name (string)
- last_name (string)
- email (string)
- num_etudiant (string)
- date_naissance (string : Day-Month-Year)
- profile (string)

à part pour la date et le profile qui doivent être entier, les autres champ peuvent être incomplet et la base cherchera les utilisateurs contenant cette chaine dans l'attribut

le profile doit correspondre à un profile défini ci dessus

la recherche des champs peuvent être cumulative

les chaines de caractères ne respectent pas la casse

Si aucun utilisateur ne correspond à la requete, cela renvoie une dataform vide

##### response

informations de ou des utilisateurs trouvés

```bash
http://127.0.0.1:8000/userSearch/

pour une requete : 
{
    "first_name" : "ben"
    "last_name" : "vre"
    "email" : "6"
    "profile" : "ENS"
}

on aura : 
[
    {
        "id": 15,
        "email": "enseignant6@po.fr",
        "first_name": "Benoit",
        "last_name": "Favre",
        "first_connection": true,
        "profile": "profile"
    },
    {
        "id": 23,
        "email": "enseignant16@po.fr",
        "first_name": "Benoit",
        "last_name": "Favre",
        "first_connection": true,
        "profile": ""
    }
]
```

## Filiere

informations d'une filiere :

- id (int) : id de la filiere
- nom (string)  : nom filiere
- nom_directeur (string): nom directeur de filiere
- prenom_directeur (string) : prenom directeur de filiere

### filiereList

accèder aux informations de toutes les filières ou créer une filière
```url
http://127.0.0.1:8000/filiereList/'
```

#### GET

accès aux informations de toutes les filières

##### response 

les informations de toutes les filieres

```bash
[
    {
        "id": 2,
        "nom": "Genie Biologique",
        "nom_directeur": "Parsiegla",
        "prenom_directeur": "Goetz"
    },
    {
        "id": 3,
        "nom": "Materiaux",
        "nom_directeur": "jean",
        "prenom_directeur": "jean"
    }
]
```

#### POST
creation d'une filière

##### requete
- nom (string) : nom filiere
- nom_directeur (string): nom directeur de filiere
- prenom_directeur (string) : prenom directeur de filiere

##### response

informations de la filiere créée

```bash
{
        "id": 2,
        "nom": "Genie Biologique",
        "nom_directeur": "Parsiegla",
        "prenom_directeur": "Goetz"
    },
```

### filiereDetails

permet d'accèder à une filiere spécifique, de la modifier ou de la supprimer

```url
http://127.0.0.1:8000/filiereDetails/<int:pk>/'
```

##### argument url

- pk (int) : id de la filiere que l'on voudra modifier

#### GET

##### response

informations de la filiere

```bash
{
    "id": 5,
    "nom": "Informatique",
    "nom_directeur": "Ayache",
    "prenom_directeur": "Stephane"
}
```

#### PUT

##### arguments requete

les informations que l'on veut modifier
si certains champ ne changement pas, il faut aussi les renvoyer : la base compare la filiere existante avec la filiere renvoyé pour voir ce qui a été modifié

##### response

```bash
{
    "id": 5,
    "nom": "Informatique",
    "nom_directeur": "Ayache",
    "prenom_directeur": "Stephane"
}
```

#### DELETE

suprime la filiere

##### response

```bash
{
    "success": "filiere supprimée avec succès"
}
```

## Promo

les informations et la création d'une promo

- id (int): id de la promo
- annee (int) : annee de la promo
- filiere (int) : id de la filiere à laquelle appartient la promo

### PromoList

```url
http://127.0.0.1:8000/promoList/'
```

#### GET

##### response

les informations de toutes les promos

```bash
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
    }
]
```

#### POST

permet de créer une promo

#### requete

- annee (int) : annee de la promo
- filiere (int) : id de la filiere à laquelle appartient la promo

##### response

les données de la promo créée

```bash
{
    "id": 6,
    "annee": 2029,
    "filiere": 2
}
```

### PromosDetails

permet d'accèder à un promo spécifique, de la modifier ou de la supprimer

```url
http://127.0.0.1:8000/promoDetails/<int:pk>/
```

##### argument url

- pk (int) : id de la promo que l'on voudra modifier

#### GET

##### response

```bash
{
    "id": 2,
    "annee": 2026,
    "filiere": 2
}
```

#### PUT

##### arguments requete

les informations que l'on veut modifier
les informations que l'on veut modifier
si certains champ ne changement pas, il faut aussi les renvoyer : la base compare la filiere existante avec la filiere renvoyé pour voir ce qui a été modifié

##### response

information de la promo avec les modifications

```bash
{
    "id": 2,
    "annee": 2026,
    "filiere": 2
}
```

#### DELETE

suprime la promo


##### response

```bash
{
    "success": "promo supprimée avec succès"
}
```

### PromoFiliere

permet d'afficher une promo associé à sa filière

```url
http://127.0.0.1:8000/promoFiliere/
```

#### GET

affiche toutes les promos avec la filiere associé

##### response

```bash
[
    {
        "id": 2,
        "annee": 2026,
        "filiere": {
            "id": 2,
            "nom": "Genie Biologique",
            "nom_directeur": "Parsiegla",
            "prenom_directeur": "Goetz"
        }
    },
    {
        "id": 4,
        "annee": 2027,
        "filiere": {
            "id": 2,
            "nom": "Genie Biologique",
            "nom_directeur": "Parsiegla",
            "prenom_directeur": "Goetz"
        }
    }
]
```

## Stage

informations d'une filiere :

- id (int) : id du stage
- sujet (string)  : sujet du stage
- nom_entreprise (string): nom de l'entreprise dans lequel se déroule le stage
- Confidentiel (booléen) : le stage est il Confidentiel ? 
- date_debut (date) : date de debut de stage
- date_fin (date) : date de fin de stage
- tuteur (int) : id du tuteur

### stageList

accèder aux informations de toutes les stages ou créer un stage
```url
http://127.0.0.1:8000/stageList/'
```

#### GET

accès aux informations de toutes les stages

##### response 

les informations de toutes les stages

```bash
[
    {
        "id": 2,
        "confidentiel": true,
        "sujet": "Gestion des cellules",
        "date_debut": "2024-01-18",
        "date_fin": "2024-08-18",
        "nom_entreprise": "Biomérieux",
        "tuteur": 3
    }
]
```

#### POST
creation d'un stage

#### Requete
- sujet (string)  : sujet du stage
- nom_entreprise (string): nom de l'entreprise dans lequel se déroule le stage
- confidentiel (booléen) : le stage est il Confidentiel ? 
- date_debut (date) : date de debut de stage
- date_fin (date) : date de fin de stage
- tuteur (int) : id du tuteur

##### response

informations du stage crée.

```bash
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

### stageDetails

permet d'accèder à une stage spécifique, de le modifier ou de le supprimer

```url
http://127.0.0.1:8000/stageDetails/<int:pk>/'
```

##### argument url

- pk (int) : id du stage que l'on voudra modifier

#### GET

##### response

informations du stage

```bash
http://127.0.0.1:8000/stageDetails/5/
   {
    "id": 5,
    "confidentiel": false,
    "sujet": "Participer au maintien d’APRIL ON au sein de l’équipe RUN",
    "date_debut": "2024-06-03",
    "date_fin": "2024-08-02",
    "nom_entreprise": "April",
    "tuteur": 31
    }
```

#### PUT

permet de modifier un stage
##### arguments requete

les informations que l'on veut modifier
si certains champ ne changement pas, il faut aussi les renvoyer : la base compare le stage existant avec le stage renvoyé pour détecter ce qui a été modifié

##### response

```bash
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

#### DELETE

suprime le stage

##### response

```bash
{
    "success": "stage supprimé avec succès"
}
```

## Soutenance

gere toutes les soutenances

### informations d'un soutenance

- "id" : id de la soutenance
- "etudiant": id de l'étudiant
- "jury": id du jury
- "stage": id du stage
- "date_soutenance": date du déroulement de la soutenance
- "heure_soutenance": heure du déroulement de la soutenance
- "note": note de la soutenance

```url
http://127.0.0.1:8000/soutenanceList/

http://127.0.0.1:8000/soutenanceDetails/<int:idSoutenance>/

```

### envoie

```bash
{
    "etudiant": 32,
    "jury": 1,
    "stage": 2,
    "date_soutenance": "03-09-2024",
    "heure_soutenance": "11:50",
    "note": 15.0
}
```

### reçu

```bash
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

# Gestion des formulaires

le formulaire est composé de plusieurs tables, Formulaire, Question, Checkbox et Reponse

Un formulaire peut avoir plusieurs questions, si la question est de type checkbox elle peut avoir plusieurs éléments checkbox, les réponses sont associès à chaque question ainsi qu'à un utilisateur

## Formulaire All

formulaire all permet de créer et gérer tous les entités d'un formualire : le formulaire, les question et les checkbox

- id (string) : id du formulaire
- title (string): titre du formulaire
- description (string) : description du formulaire

### formulaireAllList

accèder aux informations de tous les formulaires ou créer un formulaire

```url
http://127.0.0.1:8000/formulaireAllList/'
```

#### GET

accès aux informations de tous les formulaires

##### response 

les informations de toutes les stages

```bash
[
    {
        "id": "1",
        "title": "Evaluation",
        "description": "fomulaire pour l'evaluation de Louise",
        "question": [
            {
                "id": 3,
                "title": "qu'avez vous pensé de votre stage ?",
                "type": "text",
                "checkbox": []
            },
            {
                "id": 5,
                "title": "titre",
                "type": "checkbox",
                "checkbox": []
            }
        ]
    },
    {
        "id": "dedefohzeouhfzeuhfouzfuzeufz",
        "title": "Evaluationde",
        "description": "formulaire pour l'evaluation de Louise",
        "question": []
    },
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
                "type": "text",
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

#### POST

création d'un formulaire

#### Requete

- sujet (string)  : sujet du stage
- nom_entreprise (string): nom de l'entreprise dans lequel se déroule le stage
- confidentiel (booléen) : le stage est il Confidentiel ? 
- date_debut (date) : date de debut de stage
- date_fin (date) : date de fin de stage
- tuteur (int) : id du tuteur

##### response

informations du stage crée.

```bash
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

### stageDetails

permet d'accèder à une stage spécifique, de le modifier ou de le supprimer

```url
http://127.0.0.1:8000/stageDetails/<int:pk>/'
```

##### argument url

- pk (int) : id du stage que l'on voudra modifier

#### GET

##### response

informations du stage

```bash
http://127.0.0.1:8000/stageDetails/2/
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

#### PUT

permet de modifier un stage
##### arguments requete

les informations que l'on veut modifier
si certains champ ne changement pas, il faut aussi les renvoyer : la base compare le stage existant avec le stage renvoyé pour détecter ce qui a été modifié

##### response

```bash
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

#### DELETE

suprime le stage

##### response

```bash
{
    "success": "stage supprimé avec succès"
}
```

## Response

- id (string) : id de la response
- content (string): content de la response
- question (int) : id de la question associée
- user (int) : id de l'utilisateur

### ResponseList

accèder aux informations de toutes les formulaires ou créer un formulaire

```url
http://127.0.0.1:8000/responseList/'
```

#### GET

accès aux informations de tous les réponses

##### response 

les informations de toutes les réponses

```bash
[
    {
        "id": 1,
        "content": "oui",
        "question": 3,
        "user": 33
    },
    {
        "id": 2,
        "content": "oui",
        "question": 4,
        "user": 33
    },
]
```

#### POST
creation d'une réponse

#### Requete

- content (string): content de la response
- question (int) : id de la question associée
- user (int) : id de l'utilisateur

##### response

informations du stage crée.

```bash
    {
        "id": 2,
        "content": "oui",
        "question": 4,
        "user": 33
    }
```

### responseDetails

permet d'accèder à une réponse spécifique, de la modifier ou de la supprimer

```url
http://127.0.0.1:8000/responseDetails/<int:pk>/'
```

##### argument url

- pk (int) : id de la réponse que l'on voudra modifier

#### GET

##### response

informations du stage

```bash
http://127.0.0.1:8000/responseDetails/1/

    {
    "id": 1,
    "content": "oui",
    "question": 3,
    "user": 33
    }
```

#### PUT

permet de modifier une réponse
##### arguments requete

les informations que l'on veut modifier
si certains champ ne changement pas, il faut aussi les renvoyer : la base compare la réponse existante avec la  réponse renvoyée pour détecter ce qui a été modifié

##### response

```bash
{
    "id": 1,
    "content": "oui",
    "question": 3,
    "user": 33
}

```

#### DELETE

suprime la réponse

##### response

```bash
{
    "success": "response supprimée avec succès"
}
```
