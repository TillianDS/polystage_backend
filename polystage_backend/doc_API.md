# dernier ajout
- ajout de date limite au formulaire
- [sendCodeMail](#sendcodemail): envoyer le code de réinitilisation à l'utilisateur
- [verifyCode](#verifycode): vérifier la validité du code
- [changePassword](#change-password): changer le mot de passe une fois le code validé
- [getStatutFormulaire](#getstatutformulaire): avoir le status d'un formulaire pour un utilisateur
- [modifyFormulaireAll](#modifyformulaireall): modifier un formulaire
- [manageJuryMembreJury](#managejurymembrejury): gérer la relation entre les membreJury et un Jury
- [userSearch](#usersearch): recherche des utilisateurs
- [getUserSession](#getusersession): renvoie les sessions auxquels est affilié l'utilisateur connecté
- ajout de fini à la session lorsque toutes les soutenances de la session sont finit
- ajout de soutenu à la soutenance : True lorsque la soutenance a été soutenu (lorsqu'elle a reçu une note)
- [setPassword](#setpassword): changement d'un password par un superutilisateur
- [gestion des Administrateur et des Superuser](#superuser):  gestion des admin et superuser
- [importJury](#import-des-jurys): import massif des jurys
- [importStage](#import-des-stages): import massif des stages
- [importSoutenance](#import-des-soutenances): import massif des soutenances
- [importSession](#import-des-sessions): import massif des sessions
- [importUser](#import-des-utilisateurs): import massif des utilisateurs
- [validateFormulaire](#validateformulaire): valdier les informations d'un formulaire
- [saveFormulaire](#saveformulaire): sauvegarder les réponse à un formulaire
- [getFormulaireAll](#getformulaireall): permet à l'administrateur de visualiser un formulaire
- [formUser](#formuser):  renvoie toutes les informations d'un formulaire avec les réponses enregistré en fonction de l'utilisateur connecté et du stage passé en url
- changement sur les reponse au formulaire : demande maitenant du stage et non plus de l'étudiant
- [getJuryMembreJury](#getjurymembrejury): renvoie les jurys et leur session, lié au membre jury connecté
- [getSessionFiliere](#getsessionfiliere): renvoie les sessions d'une filiere
- [juryAll](#juryall) : renvoie toutes les informations du jury : ses étudiant, soutenances, stages
- [entudiantAll](#etudiantall) : obtenir toutes les informations lié a étudiant connecté
- [getStageTuteur](#getstagetuteur): renvoie les stages et étudiants suivis par le tuteur connecté
- [getInfoSession](#getinfosession) : toutes les informations d'un session
- [responseFormulaire](#responseformulaire): renvoie le formulaire et toutes ses réponses associé à un stage
- [isLeader](#isleader) : l'utilisateur connecté est il leader du jury
- [becomeLeader](#becomeleader) : devenir leader du jury
- [isJury](#isjury) : l'utilisateur connecté fait il partie d'un jury

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

## etudiantAll

renvoie l'etudiant connecté avec toutes tous ses stages, soutenances, jury et session associés

### URL

```url
http://127.0.0.1:8000/etudiantAll/
```

méthode : GET

### Permissions 

Etudiants 

### données reçues

```json
{
    "id": 50,
    "email": "etu1@po.fr",
    "first_name": "etu1",
    "last_name": "etu1",
    "first_connection": false,
    "profile": "ETU",
    "is_active": true,
    "num_etudiant": "d000001",
    "stage": [
        {
            "id": 6,
            "is_active": true,
            "soutenance": [
                {
                    "id": 3,
                    "is_active": true,
                    "jury": {
                        "id": 8,
                        "is_active": true,
                        "jury": {
                            "id": 2,
                            "nom": "info 3A 2024",
                            "filiere": 5
                        },
                        "salle": "A130",
                        "batiment": "A",
                        "campus": "Luminy",
                        "zoom": "http://",
                        "num_jury": 2,
                        "leader": 49,
                        "session": 2,
                        "membreJury": [
                            49,
                            53,
                            54
                        ]
                    },
                    "date_soutenance": "2024-06-30",
                    "heure_soutenance": "11:00:00",
                    "note": 20.0,
                    "soutenu": false
                }
            ],
            "sujet": "gestion du Run",
            "confidentiel": true,
            "date_debut": "2024-01-18",
            "date_fin": "2024-08-18",
            "nom_entreprise": "April",
            "tuteur": 30
        },
        {
            "id": 9,
            "is_active": true,
            "soutenance": [
                {
                    "id": 6,
                    "is_active": true,
                    "jury": {
                        "id": 9,
                        "is_active": true,
                        "jury": {
                            "id": 2,
                            "nom": "info 3A 2024",
                            "filiere": 5
                        },
                        "salle": "B115",
                        "batiment": "B",
                        "campus": "Luminy",
                        "zoom": "http://",
                        "num_jury": 3,
                        "leader": null,
                        "session": 2,
                        "membreJury": [
                            49,
                            54
                        ]
                    },
                    "date_soutenance": "2024-06-30",
                    "heure_soutenance": "13:00:00",
                    "note": 15.0,
                    "soutenu": false
                }
            ],
            "sujet": "Sécurité",
            "confidentiel": false,
            "date_debut": "2024-01-10",
            "date_fin": "2024-08-18",
            "nom_entreprise": "Atos",
            "tuteur": 3
        }
    ]
}
```


## stageTuteur

renvoie les stages et étudiants encadré par le tuteur connecté

### URL

```url
http://127.0.0.1:8000/stageTuteur/
```

méthode : GET

### Permissions 

Tuteurs 

### données reçues

```json
[
    {
        "id": 6,
        "is_active": true,
        "etudiant": {
            "id": 50,
            "email": "etu1@po.fr",
            "first_name": "etu1",
            "last_name": "etu1",
            "first_connection": false,
            "profile": "ETU",
            "is_active": true,
            "num_etudiant": "d000001"
        },
        "sujet": "gestion du Run",
        "confidentiel": true,
        "date_debut": "2024-01-18",
        "date_fin": "2024-08-18",
        "nom_entreprise": "April",
        "soutenu": false
    },
    {
        "id": 8,
        "is_active": true,
        "etudiant": {
            "id": 51,
            "email": "etu2@po.fr",
            "first_name": "etu2",
            "last_name": "etu2",
            "first_connection": false,
            "profile": "ETU",
            "is_active": true,
            "num_etudiant": "d000002"
        },
        "sujet": "dev d'une API",
        "confidentiel": true,
        "date_debut": "2024-01-18",
        "date_fin": "2024-08-18",
        "nom_entreprise": "Biomérieux",
        "soutenu": false
    }
]
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

# Session

## Informations d'une session

- id (int): id de la promo
- nom (string) : nom de la session
- filiere (int) : id de la filiere à laquelle appartient la promo
- fini (boolean) : toutes les soutenances de la session ont été soutenu

```json
{
    "id": 4,
    "nom": "info 3A 2024",
    "filiere": 2
}
```

## CRUD

### URL

```url
http://127.0.0.1:8000/sessionList/

http://127.0.0.1:8000/sessionDetails/<int>/
```

## getInfoSession

affiche toutes les promos avec la filiere associé

### URL

méthode : GET

```url
http://127.0.0.1:8000/getInfoSession/<int>/
```

données url : l'id de la session

### Données reçues

les informations de la session, les étudiants qui font partie de cette session ainsi que les jurys de la session

```json
{
    "id": 2,
    "nom": "info 3A 2024",
    "etudiants": [
        {
            "id": 51,
            "email": "etu2@po.fr",
            "first_name": "etu2",
            "last_name": "etu2",
            "first_connection": false,
            "profile": "ETU",
            "is_active": true,
            "num_etudiant": "d000002",
            "num_jury": 9
        },
        {
            "id": 50,
            "email": "etu1@po.fr",
            "first_name": "etu1",
            "last_name": "etu1",
            "first_connection": false,
            "profile": "ETU",
            "is_active": true,
            "num_etudiant": "d000001",
            "num_jury": 3
        },
        {
            "id": 50,
            "email": "etu1@po.fr",
            "first_name": "etu1",
            "last_name": "etu1",
            "first_connection": false,
            "profile": "ETU",
            "is_active": true,
            "num_etudiant": "d000001",
            "num_jury": 3
        }
    ],
    "jurys": [
        {
            "id": 1,
            "is_active": true,
            "salle": "A120",
            "batiment": "A",
            "campus": "Luminy",
            "zoom": "gtĝkrĝr\"",
            "num_jury": 9,
            "session": 2,
            "leader": 49,
            "membreJury": [
                18,
                19,
                20
            ]
        },
        {
            "id": 8,
            "is_active": true,
            "salle": "A130",
            "batiment": "A",
            "campus": "Luminy",
            "zoom": "http://",
            "num_jury": 2,
            "session": 2,
            "leader": 49,
            "membreJury": [
                49,
                53,
                54
            ]
        },
        {
            "id": 9,
            "is_active": true,
            "salle": "B115",
            "batiment": "B",
            "campus": "Luminy",
            "zoom": "http://",
            "num_jury": 3,
            "session": 2,
            "leader": null,
            "membreJury": [
                49
            ]
        }
    ],
    "fini": false
}
```

## getUserSession

renvoie les sessions selon l'utilisateur concerné

permet notamment aux admin de ne voir que les sessions lié à la filier à laquelle ils appartiennent
### URL

Méthode : GET

```url
http://127.0.0.1:8000/getUserSession/
```
### permissions
MembreJury : Enseignant, Professionnel, Admin

### informations reçues

#### sucess

```json
[
    {
        "id": 8,
        "is_active": true,
        "session": {
            "id": 2,
            "nom": "info 3A 2024",
            "filiere": 5
        },
        "salle": "A130",
        "batiment": "A",
        "campus": "Luminy",
        "zoom": "http://",
        "num_jury": 2,
        "leader": 49,
        "membreJury": [
            49,
            53,
            54
        ]
    },
    {
        "id": 9,
        "is_active": true,
        "session": {
            "id": 2,
            "nom": "info 3A 2024",
            "filiere": 5
        },
        "salle": "B115",
        "batiment": "B",
        "campus": "Luminy",
        "zoom": "http://",
        "num_jury": 3,
        "leader": null,
        "membreJury": [
            49,
            54
        ]
    }
]
```

# SessionFiliere

vues liées à la prom oet à la filière en même temps

## SessionFiliere

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

## getSessionFiliere

renvoie els informationsd'une filiere ainsi que toutes ses sessions

### URL 

méthode : GET

```url
getSessionFiliere/<int:id_filiere>
```
argument URL : l'id de la filiere dont on veut obtenir les sessions 

### Données reçues

toutes les promos associées

```json
{
    "filiere": {
        "id": 2,
        "nom": "Genie Biologique"
    },
    "sessions": [
        {
            "id": 1,
            "nom": "GBMA 3A 2024",
            "filiere": 2
        }
        {
            "id": 2,
            "nom": "GBMA 4A 2024",
            "filiere": 2
        }
    ]
}
```

## sessionEtudiant

renvoie tous les etudiants d'un session

méthode : GET

```url
sessionEtudiant/<int:id_session>
```

arguement url : l'id de la session

### Données reçues

toutes les étud assocudiants de la session

```json
{
    "id": 2,
    "nom": "info 3A 2024",
    "etudiants": [
        {
            "id": 50,
            "email": "etu1@po.fr",
            "first_name": "etu1",
            "last_name": "etu1",
            "first_connection": false,
            "profile": "ETU",
            "num_etudiant": "d000001",
            "sessions": [
                2
            ]
        }
    ]
}
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

## getStageTuteur

permet d'obtenir les toutes infos associés aux stages suivis par le Tuteur connecté

### URL

Méthode : GET

```url
http://127.0.0.1:8000/getStageTuteur/
```

### Permissions

Tuteur

### informations reçues

#### success

```json
[
    {
        "id": 6,
        "is_active": true,
        "etudiant": {
            "id": 50,
            "email": "etu1@po.fr",
            "first_name": "etu1",
            "last_name": "etu1",
            "first_connection": false,
            "profile": "ETU",
            "is_active": true,
            "num_etudiant": "d000001"
        },
        "soutenance": {
            "id": 3,
            "is_active": true,
            "sessions": {
                "id": 2,
                "nom": "info 3A 2024",
                "filiere": 5
            },
            "date_soutenance": "2024-06-30",
            "heure_soutenance": "11:00:00",
            "note": 20.0,
            "soutenu": false,
            "jury": 8
        },
        "sujet": "gestion du Run",
        "confidentiel": true,
        "date_debut": "2024-01-18",
        "date_fin": "2024-08-18",
        "nom_entreprise": "April"
    },
    {
        "id": 8,
        "is_active": true,
        "etudiant": {
            "id": 51,
            "email": "etu2@po.fr",
            "first_name": "etu2",
            "last_name": "etu2",
            "first_connection": false,
            "profile": "ETU",
            "is_active": true,
            "num_etudiant": "d000002"
        },
        "soutenance": {
            "id": 4,
            "is_active": true,
            "sessions": {
                "id": 2,
                "nom": "info 3A 2024",
                "filiere": 5
            },
            "date_soutenance": "2024-09-03",
            "heure_soutenance": "12:00:00",
            "note": 15.0,
            "soutenu": false,
            "jury": 1
        },
        "sujet": "dev d'une API",
        "confidentiel": true,
        "date_debut": "2024-01-18",
        "date_fin": "2024-08-18",
        "nom_entreprise": "Biomérieux"
    }
]
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
- jury: id du jury
- stage: id du stage
- date_soutenance: date du déroulement de la soutenance
- heure_soutenance: heure du déroulement de la soutenance
- note: note de la soutenance
- soutenu (boolean) : true si la soutenance a été soutenu, False sinon

```json
{
    "id" : 1,
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
    "id_soutenance" : "soutenance à laquelle on veut définir la note",
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

### informations envoyées

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

## isLeader

permet de savoir si le membreJury est le leader du Jury

### URL

Méthode : POST

```url
http://127.0.0.1:8000/isLeader/
```

### informations envoyées

```json
{
    "id_membreJury" : "id du membreJury",
    "id_jury" : "id du jury"
}
```

### informations reçues

#### sucess

```json
{
    "leader": true
}
```

#### non success

```json
{
    "leader": false
}
```


## juryAll

permet d'obtenir toutes les soutenances, stages, étudiants associés à un jury

### URL

Méthode : GET

```url
http://127.0.0.1:8000/juryAll/<int:id_jury>
```

argument requête : l'id du jury

### informations reçues

#### sucess

```json
{
    "id": 8,
    "is_active": true,
    "soutenance": [
        {
            "id": 3,
            "is_active": true,
            "stage": {
                "id": 6,
                "is_active": true,
                "etudiant": {
                    "id": 50,
                    "email": "etu1@po.fr",
                    "first_name": "etu1",
                    "last_name": "etu1",
                    "first_connection": false,
                    "profile": "ETU",
                    "is_active": true,
                    "num_etudiant": "d000001"
                },
                "sujet": "gestion du Run",
                "confidentiel": true,
                "date_debut": "2024-01-18",
                "date_fin": "2024-08-18",
                "nom_entreprise": "April",
                "tuteur": 30
            },
            "date_soutenance": "2024-06-30",
            "heure_soutenance": "11:00:00",
            "note": 20.0,
            "soutenu": false
        }
    ],
    "salle": "A130",
    "batiment": "A",
    "campus": "Luminy",
    "zoom": "http://",
    "num_jury": 2,
    "leader": 49,
    "session": 2,
    "membreJury": [
        49,
        53,
        54
    ]
}
```


## getJuryMembreJury

renvoie les jurys et leur sessions, associés au membreJury connecté

### URL

Méthode : GET

```url
http://127.0.0.1:8000/getJuryMembreJury/
```
### permissions
MembreJury : Enseignant, Professionnel

### informations reçues

#### sucess

```json
[
    {
        "id": 8,
        "is_active": true,
        "session": {
            "id": 2,
            "nom": "info 3A 2024",
            "filiere": 5
        },
        "salle": "A130",
        "batiment": "A",
        "campus": "Luminy",
        "zoom": "http://",
        "num_jury": 2,
        "leader": 49,
        "membreJury": [
            49,
            53,
            54
        ]
    },
    {
        "id": 9,
        "is_active": true,
        "session": {
            "id": 2,
            "nom": "info 3A 2024",
            "filiere": 5
        },
        "salle": "B115",
        "batiment": "B",
        "campus": "Luminy",
        "zoom": "http://",
        "num_jury": 3,
        "leader": null,
        "membreJury": [
            49,
            54
        ]
    }
]
```


## getJury

renvoie les jurys et leur sessions, associés au membreJury connecté

### URL

Méthode : GET

```url
http://127.0.0.1:8000/getJury/
```
### permissions
MembreJury : Enseignant, Professionnel

### informations reçues

#### sucess

```json
[
    {
        "id": 8,
        "is_active": true,
        "session": {
            "id": 2,
            "nom": "info 3A 2024",
            "filiere": 5
        },
        "salle": "A130",
        "batiment": "A",
        "campus": "Luminy",
        "zoom": "http://",
        "num_jury": 2,
        "leader": 49,
        "membreJury": [
            49,
            53,
            54
        ]
    },
    {
        "id": 9,
        "is_active": true,
        "session": {
            "id": 2,
            "nom": "info 3A 2024",
            "filiere": 5
        },
        "salle": "B115",
        "batiment": "B",
        "campus": "Luminy",
        "zoom": "http://",
        "num_jury": 3,
        "leader": null,
        "membreJury": [
            49,
            54
        ]
    }
]
```


## manageJuryMembreJury

permet d'ajouter ou de supprimer des membreJury d'un jury, ou un jury d'un membreJury

### URL

Méthode : POST, DELETE

```url
http://127.0.0.1:8000/manageJuryMembreJury/
```
### permissions
Admin

### Données envoyées

```json
{
    "id_membreJury": "id du membreJury concerné",
    "id_jury" :"id du jury concerné"
}
```

### informations reçues

#### sucess

```json
POST:
{
    "success": "le membreJury  49 a été ajouté avec succès au jury 6"
}

DELETE: 
{
    "success": "le membreJury  49 a bien été dissocié du jury 6"
}
```

# Authentification

## login

permet d'authentifier l'utilisateur et de le connecter à l'application

```url
http://127.0.0.1:8000/login/
```

méthode : POST

### Données envoyées

```json
{
    "email" : "email de l'utilisateur",
    "password" : "mot de passe"
}
```


### Données reçues

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

## sendCodeMail

envoie un mail à l'utilisateur avec son code de réinitilisation du mot de pass, s'il existe.
si l'utilisateur n'existe pas, on a le même message de succès mais aucun mail n'est envoyé

```url
http://127.0.0.1:8000/sendCodeMail/
```

methode : POST

### Données envoyées

l'email de l'utilisateur qui 
```json
{
    "email" : "email de l'utilisateur"
}
```

### Données reçues

```json
{
    "success": "email envoyé avec succès"
}
```


## verifyCode

```url
http://127.0.0.1:8000/verifyCode/
```

methode : POST

### Données envoyées


```json
{
    "email" : "email de l'utilisateur",
    "code" : "le code a vérifie"
}
```

### Données reçues

#### success
```json
    true
```

#### non success
```json
{
    "error" :"le code n'est pas valide"
}
```

## change password

permet de changer modifier le mot de passe d'un utilisateur

```url
http://127.0.0.1:8000/password/
```

méthode : POST

### Données reçues

```json
{
    "email" : "email de l'utilisateur",
    "code" : "le code a vérifie",
    "password1" : "mdp de l'utilisateur",
    "password2" : "mdp de l'utilisateur"

}
```
les password doivent contenir une majuscule, une minuscule, un caractère spécial parmis [()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?] et doivent avoir uen longueur d'au moins 7 caractères

### Données reçues

informations de l'utilisateur

```json
    {
        "id": 21,
        "email": "enseignant14@po.fr",
        "first_name": "Benoit",
        "last_name": "Favre",
        "first_connection": false,
        "profile": "ENS"
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
- id : id du formulaire
- titre (string) : titre du formulaire 
- description (string)
- session (int) : session à laquelle est rattaché le formulaire 
- date_limite (date, format : 23-11-2025 09:50:37): date limite de réponse au formulaire 
- profile (profile): profile de l'utilisateur a qui est déstiné ce formulaire (TUT, ETU, JUR)
- langue (string) : la lanque dans laquelle est le formulaire (FR, AN)
    
## CRUD

```url
http://127.0.0.1:8000/formulaireList/
http://127.0.0.1:8000/formulaireDetails/<int>/
```

# ResponseForm

### Informations d'un réponse

- id (string) : id de la response
- content (string): contenu de la response
- question (int) : id de la question associée
- stage (int) : id du stage auquel est lié la réponse

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

## formUser

tuteur ou étudiant : si le stage est soutenu, renvoie tous les formulaire lié à la session du stage, sinon renvoie juste les formulaires lié à son role

jury: renvoie tous les formulaires lié à la session

### URL

```url
http://127.0.0.1:8000/formUser/<int:id_stage>
```

méthode : GET

### Données reçues

```json
[
    {
        "id": "id",
        "titre": "Avis du tuteur",
        "description": "formulaire pour l'evaluation de Louise",
        "profile": "ETU",
        "langue": "FR",
        "session": 2
    },
    {
        "id": "formulaire",
        "titre": "soutenance de stage",
        "description": "evaluation du jury",
        "profile": "ETU",
        "langue": "FR",
        "session": 2
    },
    {
        "id": "formulaire_checkbox",
        "titre": "soutenance de stage",
        "description": "evaluation du jury",
        "profile": "ETU",
        "langue": "FR",
        "session": 2
    },
    {
        "id": "formu",
        "titre": "soutenance de stage",
        "description": "evaluation du jury",
        "profile": "ETU",
        "langue": "FR",
        "session": 2
    }
]
```

## ResponseFormulaire

renvoie le formulaire, les questions et checkbox associés en fonction du stage concerné et de l'utilisateur connecté

### URL

```url
http://127.0.0.1:8000/responseFormulaire/
```

### Données envoyées

```json
{
    "id_stage" : "id du stage associé",
    "id_formulaire" : "id du formulaire souhaité"
}
```

### Données reçues

```json
{
    "id": "id",
    "titre": "Avis du tuteur",
    "description": "formulaire pour l'evaluation de Louise",
    "session": 2,
    "profile": "ETU",
    "langue": "FR",
    "question": [
        {
            "id": 4,
            "titre": "qu'avez vous pensé de votre stage ??",
            "type": "text",
            "obligatoire": true,
            "response": {
                "id": 4,
                "stage": 6,
                "content": "le stage s'est très bien passé"
            },
            "checkbox": []
        },
        {
            "id": 6,
            "titre": "vous êtes vous ennuyé ?",
            "type": "checkbox",
            "obligatoire": true,
            "response": null,
            "checkbox": [
                {
                    "id": 1,
                    "titre": "Oui",
                    "response": {
                        "id": 2,
                        "stage": 6,
                        "valeur": false
                    }
                },
                {
                    "id": 2,
                    "titre": "Non",
                    "response": {
                        "id": 5,
                        "stage": 6,
                        "valeur": false
                    }
                }
            ]
        },
        {
            "id": 7,
            "titre": "qu'avez vous pensé du stagiaire ?",
            "type": "text",
            "obligatoire": true,
            "response": {
                "id": 8,
                "stage": 6,
                "content": "i a été tres entreprenant"
            },
            "checkbox": []
        }
    ]
}
```

### non success

- le formulaire n'existe pas
- le stage n'existe pas
- l'utilisateur (etudiant, tuteur) ne sont pas associés à ce stage
- le formulaire n'est pas encre accessible à l'etudiant ou le tuteur

# Autres endpoints formulaire

## getFormulaireAll

getFormulaireAll permet à un admin de récupérer l'ensemble des informations d'un formulaire : l'entité formulaire avec les questions et les checkbox 

### URL

methode : GET

```url
http://127.0.0.1:8000/getFormulaireAll/<str:pk>/
```

pk : la clé primaire du formulaire

### Permissions :

Admin

### données reçues

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
    "id": "id",
    "date_limite": "23-11-2025 09:50:37",

    "question": [
        {
            "id": 4,
            "titre": "qu'avez vous pensé de votre stage ??",
            "type": "text",
            "checkbox": [],
            "obligatoire": true
        },
        {
            "id": 6,
            "titre": "vous êtes vous ennuyé ?",
            "type": "checkbox",
            "checkbox": [
                {
                    "id": 1,
                    "titre": "Oui"
                },
                {
                    "id": 2,
                    "titre": "Non"
                }
            ],
            "obligatoire": true
        },
        {
            "id": 7,
            "titre": "qu'avez vous pensé du stagiaire ?",
            "type": "text",
            "checkbox": [],
            "obligatoire": true
        }
    ],
    "titre": "Avis du tuteur",
    "description": "formulaire pour l'evaluation de Louise",
    "profile": "ETU",
    "langue": "FR",
    "session": 2
}
```

## modifyFormulaireAll

permet de modifier un formulaire en envoyant toutes les informations en même temps

### URL

```url
http://127.0.0.1:8000/modifyFormulaireAll<str:id_formulaire>/
```

méthode : PUT

donnée url : id du formulaire que l'on souhaite modifier
### permissions

Admin

### Données envoyées

```json
{
    "id": "id",
    "question": [
        {
            "id": 4,
            "titre": "qu'avez vous pensé de votre stage ??",
            "type": "text",
            "checkbox": [],
            "obligatoire": true
        },
        {
            "id": 6,
            "titre": "vous êtes vous ennuyé ?",
            "type": "checkbox",
            "checkbox": [
                {
                    "id": 1,
                    "titre": "Oui"
                },
                {
                    "id": 2,
                    "titre": "Non"
                }
            ],
            "obligatoire": true
        },
        {
            "id": 7,
            "titre": "qu'avez vous pensé du stagiaire ?",
            "type": "text",
            "checkbox": [],
            "obligatoire": true
        }
    ],
    "date_limite": "23-11-2025 09:50:37",
    "titre": "Avis du tuteur",
    "description": "formulaire pour l'evaluation de Louise",
    "profile": "ETU",
    "langue": "FR",
    "session": 2
}
```

### Données reçues

retourne le formulaire enregistré
```json
{
    "id": "id",
    "question": [
        {
            "id": 4,
            "titre": "qu'avez vous pensé de votre stage ??",
            "type": "text",
            "checkbox": [],
            "obligatoire": true
        },
        {
            "id": 6,
            "titre": "vous êtes vous ennuyé ?",
            "type": "checkbox",
            "checkbox": [
                {
                    "id": 1,
                    "titre": "Oui"
                },
                {
                    "id": 2,
                    "titre": "Non"
                }
            ],
            "obligatoire": true
        },
        {
            "id": 7,
            "titre": "qu'avez vous pensé du stagiaire ?",
            "type": "text",
            "checkbox": [],
            "obligatoire": true
        }
    ],
    "date_limite": "23-11-2025 09:50:37",
    "titre": "Avis du tuteur",
    "description": "formulaire pour l'evaluation de Louise",
    "profile": "ETU",
    "langue": "FR",
    "session": 2
}-
```

## saveFormulaire

sauvegarder un formulaire en enregistrant toutes les réponse apssé en paramètre et en passant la statut du stage lié à ce formulaire en "sauvegarde"

### URL

methode : POST

```url
http://127.0.0.1:8000/saveFormulaire/
```

### données envoyées

- toutes les informations du formulaire avec les questions et réponse. Si la réponse existe déjà on la renvoie avec son id, sinon on renvoie sans id (et la réponse est créer)

- l'id du stage pour lequel sont enregistrés les reponses au formulaire (sera inclu automatiquement dans les nouvelles réponses)

- si une réponse existe déjà, la réponse sera cherché et modifié, vous n'avez pas besoin d'inclure l'id de la réponse

```json
{ 
    "formulaire": 
    {
    "id": "id",
    "titre": "Avis du tuteur",
    "description": "formulaire pour l'evaluation de Louise",
    "session": 2,
    "profile": "ETU",
    "langue": "FR",
    "question": [
        {
            "id": 4,
            "titre": "qu'avez vous pensé de votre stage ?",
            "type": "text",
            "response":
                {
                    "content": "le stage s'est très bien passé"
                },
            "checkbox": []
        },
        {
            "id": 6,
            "titre": "vous êtes vous ennuyé ?",
            "type": "checkbox",
            "response": [],
            "checkbox": [
                {
                    "id": 1,
                    "titre": "Oui",
                    "response": 
                        {
                            "id": 2,
                            "stage": 6,
                            "valeur": false
                        }
                    
                },
                {
                    "id": 2,
                    "titre": "non",
                    "response":
                        {
                            "valeur": false
                        }
                }
            ]
        },
        {
            "id": 7,
            "titre": "qu'avez vous pensé du stagiaire ?",
            "type": "text",
            "response": {
                "content" : "il a été très entreprenant et tres pro"
            },
            "checkbox": []
        }
    ]
},
    "id_stage" : 6
}
```

## validateFormulaire

valider un formulaire en enregistrant toutes les réponse et en passant la statut du stage lié à ce formulaire en "rendu"

### URL

methode : POST

```url
http://127.0.0.1:8000/validateFormulaire/
```

### données envoyées

- toutes les informations du formulaire avec les questions et réponse. Si la réponse existe déjà on la renvoie avec son id, sinon on renvoie sans id (et la réponse est créer)

- l'id du stage pour lequel sont enregistrés les reponses au formulaire (sera inclu automatiquement dans les nouvelles réponses)

- si une réponse existe déjà, la réponse sera cherché et modifié, vous n'avez pas besoin d'inclure l'id de la réponse

```json
{ 
    "formulaire": 
    {
    "id": "id",
    "titre": "Avis du tuteur",
    "description": "formulaire pour l'evaluation de Louise",
    "session": 2,
    "profile": "ETU",
    "langue": "FR",
    "question": [
        {
            "id": 4,
            "titre": "qu'avez vous pensé de votre stage ?",
            "type": "text",
            "response":
                {
                    "content": "le stage s'est très bien passé"
                },
            "checkbox": []
        },
        {
            "id": 6,
            "titre": "vous êtes vous ennuyé ?",
            "type": "checkbox",
            "response": [],
            "checkbox": [
                {
                    "id": 1,
                    "titre": "Oui",
                    "response": 
                        {
                            "id": 2,
                            "stage": 6,
                            "valeur": false
                        }
                    
                },
                {
                    "id": 2,
                    "titre": "non",
                    "response":
                        {
                            "valeur": false
                        }
                }
            ]
        },
        {
            "id": 7,
            "titre": "qu'avez vous pensé du stagiaire ?",
            "type": "text",
            "response": {
                "content" : "il a été très entreprenant et tres pro"
            },
            "checkbox": []
        }
    ]
},
    "id_stage" : 6
}
```

### données reçues

#### sucess

```json
{
    "sucess": "tout a été enregistré avec succès"
}
```

#### error

si le systeme rencontre une erreur, les données réponse qui ne sont pas en erreur sont enregistré et les autres sont renvoyé

- s'il manque une réponse et que la réponse à la question est obligatoire, renvoie la question à laquelle il manque une réponse

- si l'id passé d'une réponse ne correspond à aucun réponse enregistré

- si l'utilisateur qui accède à la vue ne pas lié au stage ou au formulaire

- s'il y'a un probleme lors de l'enregistrement du serialiseur

- si le formulaire a déjà été rendu

- la date limite est dépassé

```json
{
    "error": [
        {
            "question": "question en erreur",

            "error": "raison de l'erreur"
        }
    ],
    "message": "ces questions ont recontrés des erreurs et n'ont pas été enregistré"
}
```


## getStatutFormulaire

retourne le statut du questionnaire pour un utilisateur

### URL

methode : POST

```url
http://127.0.0.1:8000/getStatutFormulaire/
```

### données envoyées

```json
{
    "id_user" :"id de l'utilisateur",
    "id_formulaire":"id du formulaire"
}
```

### données reçues

#### sucess

```json
    {
        "status":"rendu"
    }
```

# Import des données

## Fonctionnement

Permet d'importer des données massivement, sous format JSON. Si l'instance importé existe déjà dans la base cela modifie ses informations par rapport à celle envoyées. Si l'instance est inactive, cela la rend active.

### Permissions 

Administrateurs

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
        "num_etudiant" : "d22014217"
    }
]
```

### Données reçues

#### success

```json
{
    "success" : "tous les utilisateurs ont été importé avec succés"
}
```

#### non success

- le profile n'est pas le bon
- un utilisateur avec ce mail existe avec un profile différent
- problème lors de l'enregistrement lié au format des données
- champ non spécifié
- unicité de l'adresse mail ou du num_etudiant
- enregistrement de profile non autorisé (ADM, SPR)


## Import des Stages

### URL

```url
http://127.0.0.1:8000/importStage/
```

méthode : POST

### Permissions

Administrateurs

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

#### non sucess

## Import des Sessions

importe des sessions associé à la filiere de l'administreteur connecté

```url
http://127.0.0.1:8000/importSession/
```

méthode : POST

### Permissions

Administrateurs

### Données à envoyer

```json
[
    {
       
        "nom": "info 3A 2024"
    },

    {
       
        "nom": "info 3A 2025"
    }
]
```

### Données reçues

#### non success 

- un session avec ce nom existe deja dans la filiere de l'administrateur
- problème avec le format des données lors de l'enregistrement

## Import des Soutenances

import en masse des soutenances

```url
http://127.0.0.1:8000/importSoutenance/
```

méthode : POST

### Permissions

Administrateurs

### Données à envoyer
- num_convention : le numéro de convention du stage auquel associé la soutenance
- nom_session : le nom de la session dans lequel se déroulera cette soutenance
- num_jury : le numéro du jury au sein de la session 

```json
[
    {
        "num_convention" : 80808,
        "nom_session" :"Info 3A 2024",
        "date_soutenance" :"30-06-2024",
        "heure_soutenance" : "10:00",
        "num_jury" : "3"
    },
    {
        "num_convention" : 808081,
        "nom_session" :"Info 5A 2024",
        "date_soutenance" :"30-06-2024",
        "heure_soutenance" : "11:00",
        "num_jury" : "2"
    }
    
]
```

### Données reçues

#### non success 
- problème de format sur les données
- la session n'existe pas 
- le stage n'existe pas
- le jury n'exsite pas

## Import des Jurys

import en masse des jury associés au membre qui les compose

```url
importJury/
```
méthode : POST

### Données à envoyer

si certaines informations du jury ne sont pas encor disponible, comme le lieu de passage ou le lien zoom, il est possible de ne pas spécifier ces informations

```json
[
    {
        //information sur le jury
        "jury" : { 
            "nom_session" :"info 3A 2024",
            "num_jury" : 3
        },
        //liste des adresses mails des membreJury faisant partie de ce jury
        "membresJury" : [
            "ben3@po.fr"
        ]
    },
    {
        //information sur le jury
        "jury" : { 
            "nom_session" :"info 3A 2024",
            "num_jury" : 3,
            "zoom" : "http://...",
            "batiment":"A",
            "campus":"Luminy",
            "salle": "127"

        },
        //liste des adresses mails des membreJury faisant partie de ce jury
        "membresJury" : [
            "ben3@po.fr",
            "mp@po.fr",
            "yvesJehanno@po.fr"
        ]
    }
]
```

### Données reçues

#### non success

- il manque des informations sur le jury ou sur les membres jurys
- les adresse mail ne correspondent à aucun membreJury
- le nom de la session ne correspond à aucune session active
- problème lors de l'enregistrement du serializer (manque d'information ou intégrité des données)

# Search

rechercher dans les différentes tables selon un / des critères souhaité

## userSearch

recherche un utilisateur selon son nom, prénom, email ou numéro étudiant (si étudiant). Le champ n'a pas besoin d'être entier, on regarde dans chaque colonne pour chaque utilisaterur si un champ contient la propriété recherché. Il est possible de rajouter dans requêt un champ profile pour faire la recherche uniquement sur ce profile concerné

```url
userSearch/
```

méthode : POST

### Permissions

Administrateurs

### Données à envoyer

```json
{
    "search" :  "champ à chercher",
    "profile" : "profile de l'utilsiateur" //option
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
```json
envoie : 
{
    "search" :  "",
    "profile" : "TUT"
}

reçus :
    [
        {
        "id": 30,
        "email": "tuteur2@po.fr",
        "first_name": "tuteur",
        "last_name": "tuteur",
        "first_connection": false,
        "profile": "TUT",
        "is_active": true
        },
        {
            "id": 31,
            "email": "Louise@po.fr",
            "first_name": "Louise",
            "last_name": "Runavot",
            "first_connection": false,
            "profile": "TUT",
            "is_active": true
        },
        {
            "id": 35,
            "email": "test@po.fr",
            "first_name": "",
            "last_name": "jean",
            "first_connection": true,
            "profile": "TUT",
            "is_active": true
        }
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

# SuperUser

endpoint de gestion pour un super utilisateur

## Gestion Administrateur
enregister un administrateur ou afficher la liste des adminsitrateur

### CRUD 

```url
http://127.0.0.1:8000/adminList/
methode : GET, POST

http://127.0.0.1:8000/adminList/<int:id_administrateur>/
methode : PUT, DELETE
```

!! contrairement aux autres vues, le delete est un hard_delete : suppression définitive

### Permissions

superutilisateurs : 'SPR'

### Données Administrateur

```json
{
    "email" : "email@po.fr",
    "first_name" : "fisrt_name",
    "last_name" :"last_name",
    "password1" : "Password*",
    "password2" : "Password*"
}
```

## Gestion super utilisateur

gérer les super utilisateur

### CRUD 

```url
http://127.0.0.1:8000/superUserList/
methode : GET, POST

http://127.0.0.1:8000/superUserDelete/<int:id_superuser>/
methode : DELETE
```

!! contrairement aux autres vues, le delete est un hard_delete : suppression définitive

### Permissions

superutilisateurs : 'SPR'

### Données SuperUser

```json
{
    "email" : "email@po.fr",
    "first_name" : "fisrt_name",
    "last_name" :"last_name",
    "password1" : "Password*",
    "password2" : "Password*"
}
```

## SetPassword

définir un password pour un utilisateur

```url
http://127.0.0.1:8000/setPassword/
```

methode : POST

!!! pas de vérification de la validité du password

### Permissions

superutilisateurs : 'SPR'

### Données envoyées

```json
{
    "email" : "email@po.fr",
    "password" : "Password*"
}
```


## derogationLogin

permet à un superutilisateur de s'authentifier en se dérogeant à un autre utilisateur

```url
http://127.0.0.1:8000/derogationLogin/
```

methode :  POST

### Données envoyées

l'email de l'utlisateur auquel on veut se déroger

```json
{
    "email" : "email de l'utilisateur"
}
```

### Données reçues

#### success
si le mail est correct:

- "id" : identifiants utilisateurs
- "type utilisateur" : type de l'utilisateur qui se connecte

```json
{
    "user_id": 14,
    "profile": "ADM"
}
```

### non successs

```json
{
    "error" : "l'adresse spécifié ne correspond à aucun utilisateur"
}
```

