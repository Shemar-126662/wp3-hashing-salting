# Test Correct Leerlingen Analyse

Dit project is een website voor het visualiseren van leerresultaten en voortgang van leerlingen. De applicatie geeft inzicht in voortgang per leerdoel, vak, kernwoord en taxonomieniveau en bevat daarnaast een docentweergave voor klasbrede analyse. De gegevens zijn fijn verwerkt in grafieken en tabellen voor verbeterde overzicht.

## Functionaliteiten

- Leerlingenoverzicht met de studenten.
- Studentendashboard met vakken, leerdoelen en voortgangsscores.
- Overzicht per leerdoel.
- Snapshot-overzicht per student en vak.
- Docentdashboard met klasoverzicht, gemiddelde score en zwakke gebieden.
- Analysepagina voor leerdoelen


## Projectstructuur

```text
.
|-- app.py
|-- import_data.py
|-- data/
|   `-- database.py
|-- routes/
|   |-- student_routes.py
|   `-- teacher_routes.py
|-- templates/
    |--...
|-- static/
|   |-- css/
|   |-- js/
|   `-- images/
|-- data-sample.zip
|-- data-sample.json
`-- student.db
```

## Installatie

1. installeer Python 3.10 of nieuwer

2. Installeer Flask:

```powershell
pip install -r requirements.txt
```

## Applicatie starten

Start de app vanuit de terminal met:

```powershell
python app.py
```

De website draait daarna standaard op:

```text
http://127.0.0.1:5000
```

Login voor docenten:

```
EMAIL / WACHTWOORD
• louella@admin.com / louella123
• lars@admin.com / lars123
• sietze@admin.com / sietze123
• diederik@admin.com / diederik123
```
Login voor studenten (per student):
```
EMAIL / WACHTWOORD
• milan@test.com / milan123
• emma@test.com / emma123
• jamie@test.com / jamie123
• lotte@test.com / lotte123
• sam@test.com / sam123
• daan@test.com / daan123
• robin@test.com / robin123
• noah@test.com / noah123
• taylor@test.com / taylor123
• alex@test.com / alex123
```

## Belangrijkste routes

### Pagina's

- landingspagina
- loginpagina
- lijst met studenten
- dashboard van een student
- detailpagina van een leerdoel
- snapshots van een student
- docentdashboard
- analyse van leerdoelen op klasniveau

## Database-overzicht

De database bevat onder andere de volgende tabellen:

- `students`
- `subjects`
- `learning_goals`
- `keywords`
- `learning_goal_keywords`
- `student_subjects`
- `snapshots`
- `taxonomy_scores`

## Opmerking

De applicatie start met debug uit. Stel voor een vaste sessiesleutel de omgevingsvariabele `SECRET_KEY` in.


## BRONNEN
## SHEMAR BRAAFHEID:
https://chatgpt.com/g/g-p-697a2f3e89a48191a1ea59b971b36c60
https://www.w3schools.com/bootstrap5/



## Hashing en salting

Nieuwe studentaccounts kun je aanmaken via `/register` (minimaal 12 tekens).
Registratie en de import van fictieve accounts bewaren alleen Argon2id-hashes.
`security.py` gebruikt 64 MiB geheugen, 3 iteraties, parallelisme 4 en een
willekeurige salt van 16 bytes. De salt en instellingen staan in de hash in
`users.password_hash` (TEXT). Inloggen controleert met `verify()` en vernieuwt
verouderde hashinstellingen na een geslaagde controle.

### Bestaande database

Stop de app. Voer vanuit de projectmap `python migrate_passwords.py` uit voordat
je een oude database opent met deze versie. De migratie hasht de bestaande
wachtwoorden, behoudt gebruikers-ID's en verwijdert de oude kolom `password`.
Een tweede uitvoering verandert niets. Hiervoor is SQLite 3.35 of nieuwer nodig.
Oude exports, backups en kopieën kunnen nog leesbare wachtwoorden bevatten;
lever die niet mee in. Gebruik voor deze opdracht alleen fictieve accounts.
De voorbeeldwachtwoorden in dit project en README zijn openbare testgegevens.

### Controleren

Voer `python -m unittest discover -s tests -v` uit. De tests gebruiken tijdelijke
databases en controleren registratie, import, goede en foute logins, onbekende
accounts, unieke salts, ongeldige hashes en migratie van de oude database.
De controle op loguitvoer geldt voor de geteste import. De gewijzigde code
logt geen wachtwoorden; externe serverlogs zijn niet in deze test meegenomen.

### Eigen repository

Deze lokale kopie behoudt de geschiedenis van de schoolrepository. Maak op
GitHub onder je eigen account een lege repository zonder README. Verbind deze
vervolgens vanuit deze map (vervang de URL door die van je nieuwe repository):

```sh
git remote rename origin upstream
git remote add origin https://github.com/Shemar-126662/NAAM-VAN-JE-REPOSITORY.git
git push -u origin feature/hashing-salting
```

De bestaande schoolrepository wordt hierbij niet aangepast. De commit-ID blijft
hetzelfde na het pushen. Een lokale kopie alleen voldoet nog niet aan de eis van
een eigen online repository.
