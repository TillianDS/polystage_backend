
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

les informations de l'utilisateur :

- id (int) : identfifiant de l'utilisateur
- first_name (string) : prenom
- last_name (string) : prenom
- first_connection (boolean): est ce la première connection de l'utilisateur
- profile (string: profile) : profile du user

pour les etudiants on trouve en plus :

- num_etudiant (int) : numéro de l'etudiant
- date_naissance (date) : date de naissance de l'etudiant

### login

permet d'authentifier l'utilisateur et de la connecter à l'application

```url
http://127.0.0.1/login/
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

### change password

permet de changer modifier le mot de passe d'un utilisateur
le mot de passe doit contenir une majuscule, une minuscule, un caractère spécial et doit avoir une taille minimum de 7 caractères

```url
http://127.0.0.1/password/<int:pk>/
```
##### argument url

- pk (int) : id de l'utilisateur pour lequel on change le mdp

#### POST

##### arguments requete

- "password1" : nouveau mot de passe
- "password2" : vérification du mot de passe

##### response

- informations de l'utilisateur

## Filiere

informations d'une filiere :

- id (int) : id de la filiere
- nom (string)  : nom filiere
- nom_directeur (string): nom directeur de filiere
- prenom_directeur (string) : prenom directeur de filiere

### filiereList

accèder aux informations de toutes les filières ou créer une filière
```url
http://127.0.0.1/filiereList/'
```

#### GET

accès aux informations de toutes les filières

##### response 

les informations de toutes les filires


#### POST
creation d'une filière

##### requete
- nom (string) : nom filiere
- nom_directeur (string): nom directeur de filiere
- prenom_directeur (string) : prenom directeur de filiere

##### response

informations de la filiere créée

### filiereDetails

permet d'accèder à une filiere spécifique, de la modifier ou de la supprimer

```url
http://127.0.0.1/filiereDetails/<int:pk>'
```

##### argument url

- pk (int) : id de la filiere que l'on voudra modifier

#### GET

##### response

- informations de la filiere

#### PUT

##### arguments requete

- les informations que l'on veut modifier
- mais aussi celles qui ne changent pas

##### response

- informations de la filiere

#### DELETE

suprime la filiere

##### response

- success : message de succès

## Promo

les informations d'une promo

- id (int): id de la promo
- annee (int) : annee de la promo
- filiere (int) : id de la filiere à laquelle appartient la promo

### PromoList

```url
http://127.0.0.1/promoList/'
```

### PromosDetails

permet d'accèder à un promo spécifique, de la modifier ou de la supprimer

```url
http://127.0.0.1/promoDetails/<int:pk>/
```

#### GET

##### response

- les informations de toutes les promos

##### argument url

- pk (int) : id de la promo que l'on voudra mofifier

#### GET

##### response

- informations de la promo

#### PUT

##### arguments requete

- les informations que l'on veut modifier
- mais aussi celles qui ne changent pas

##### response

- informations de la promo

#### DELETE

suprime la promo

##### response

- success : message de succès