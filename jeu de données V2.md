# utilisateurs 

## Etudiants

```json
{
    "id": 71,
    "email": "etudiant1@po.fr",
    "first_name": "etudiant1",
    "last_name": "etudiant1",
    "num_etudiant": "d001",
    "password" : "Password*"

}
{
    "id": 72,
    "email": "etudiant2@po.fr",
    "first_name": "etudiant2",
    "last_name": "etudiant2",
    "num_etudiant": "d002",
    "password" : "Password*"

}
{
    "id": 73,
    "email": "etudiant3@po.fr",
    "first_name": "etudiant3",
    "last_name": "etudiant3",
    "num_etudiant": "d003",
    "password" : "Password*"

}
```

## Tuteur

```json
{
    "id": 76,
    "email": "tuteur3@po.fr",
    "first_name": "tuteur",
    "last_name": "tuteur",
    "profile": "TUT",
    "password" : "Password*"
}
{
    "id": 77,
    "email": "tuteur4@po.fr",
    "first_name": "tuteur4",
    "last_name": "tuteur4",
    "profile": "TUT",
    "password" : "Password*"

}
```

## Jury

```json
{
    "id": 74,
    "email": "benoit.favre@po.fr",
    "first_name": "Benoit",
    "last_name": "Favre",
    "profile": "ENS",
    "password" : "Password*"
}
{
    "id": 78,
    "email": "enseignant1@po.fr",
    "first_name": "ens",
    "last_name": "ens",
    "profile": "ENS",
    "password" : "Password*"
}
{
    "id": 75,
    "email": "Yves.jehanno@po.fr",
    "first_name": "Yves",
    "last_name": "Jehanno",
    "profile": "PRO",
    "password" : "Password*"
}
```

## Administrateur
```json
{
    "id": 68,
    "email": "administrateur@po.fr",
    "first_name": "adm",
    "last_name": "adm",
    "password" : "Password*",
    "filiere": 7
}
```

# Session

```json
{
    "id": 5,
    "nom": "GBM 2025",
    "status": 2, //status démarré
    "filiere": 7
}
{
    "id": 6,
    "nom": "GBM 2026",
    "status": 2,
    "filiere": 7
}
```
# Jury

```json
{
    "id": 10,
    "salle": "A130",
    "batiment": "A",
    "campus": "Luminy",
    "zoom": "http://",
    "num_jury": 1,
    "session": 5,
    "leader": null,
    "membreJury": [
        74,
        75
    ]
}
{
    "id": 11,
    "salle": "A130",
    "batiment": "A",
    "campus": "Luminy",
    "zoom": "http://",
    "num_jury": 2,
    "session": 6,
    "leader": null,
    "membreJury": [
        74,
        75,
        78
    ]
}
```

# Stage

```json
{
    "id": 11,
    "date_debut": "18-01-2024",
    "date_fin": "18-08-2024",
    "sujet": "Création de matériel biomédical",
    "confidentiel": false,
    "nom_entreprise": "Biomérieux",
    "num_convention": 1,
    "tuteur": 76,
    "etudiant": 71
}
{
    "id": 12,
    "date_debut": "18-01-2024",
    "date_fin": "18-08-2024",
    "sujet": "Etudes des IRM",
    "confidentiel": false,
    "nom_entreprise": "Biomérieux",
    "num_convention": 2,
    "tuteur": 76,
    "etudiant": 72
}
{
    "id": 13,
    "is_active": true,
    "date_debut": "18-01-2024",
    "date_fin": "18-08-2024",
    "sujet": "Etudes des IRM",
    "confidentiel": true,
    "nom_entreprise": "CHU Marseille",
    "num_convention": 3,
    "tuteur": 77,
    "etudiant": 73
}
{
    "id": 14,
    "date_debut": "18-01-2024",
    "date_fin": "18-08-2024",
    "sujet": "Maintenance des appareils",
    "confidentiel": true,
    "nom_entreprise": "CHU Marseille",
    "num_convention": 4,
    "tuteur": 77,
    "etudiant": 71
}
```

# Soutenance

```json
{
    "id": 8,
    "date_soutenance": "30-09-2024",
    "heure_soutenance": "13:00",
    "note": null,
    "soutenu": false,
    "jury": 10,
    "stage": 11
}
{
    "id": 9,
    "date_soutenance": "30-09-2024",
    "heure_soutenance": "14:00",
    "note": null,
    "soutenu": false,
    "jury": 10,
    "stage": 12
}
{
    "id": 10,
    "date_soutenance": "30-09-2024",
    "heure_soutenance": "15:00",
    "note": null,
    "soutenu": false,
    "jury": 10,
    "stage": 13
}
{
    "id": 11,
    "date_soutenance": "30-10-2023",
    "heure_soutenance": "15:00",
    "note": null,
    "soutenu": false,
    "jury": 11,
    "stage": 14
}
```

# filiere

```json
{
    "id": 7,
    "nom": "Génie Biomédical"
}
```

# formulaires 

```json
{
    "id" : "biomed 2024",
    "profile" : "TUT",
    "session" : 5
}
{
    "id" : "biomed 2024 JURY",
    "profile" : "JUR",
    "session" : 5
}
{
    "id" : "biomed 2024 ETU",
    "profile" : "ETU",
    "session" : 5
}

//soutennace finit
{
    "id" : "biomed 2023 ETU",
    "profile" : "ETU",
    "session" : 6
}
{
    "id" : "biomed 2023 TUT",
    "profile" : "TUT",
    "session" : 6
}
{
    "id" : "biomed 2023 JUR",
    "profile" : "JUR",
    "session" : 6
}
```