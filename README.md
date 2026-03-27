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
pip install flask
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

De applicatie draait in `debug=True` in `app.py`. 
