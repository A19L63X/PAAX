import json
import re

# Cargar los datos de last_standings.json
with open('data/last_standings.json', 'r') as f:
    standings = json.load(f)

# Cargar los datos de tracks2025.json
with open('data/tracks2025.json', 'r') as f:
    tracks = json.load(f)

# Diccionario de alias de pilotos
alias = {
    "Kimi Antonelli": "Andrea Kimi Antonelli"
}

# Banderas de los equipos (constructores)
banderas_constructores = {
    "Red Bull Racing": "flag_of_austria",
    "McLaren": "united_kingdom",
    "Kick Sauber": "flag_of_switzerland",
    "Racing Bulls": "flag_of_italy",
    "Alpine": "flag_of_france",
    "Mercedes": "flag_of_germany",
    "Aston Martin": "united_kingdom",
    "Ferrari": "flag_of_italy",
    "Williams": "united_kingdom",
    "Haas F1 Team": "flag_of_the_united_states"
}

# Banderas de los Grandes Premios
banderas_gp = {
    "Bahrain": "flag_of_bahrain",
    "China": "flag_of_china",    
    "Saudi Arabia": "flag_of_saudi_arabia",
    "Australia": "flag_of_australia",
    "Azerbaijan": "flag_of_azerbaijan",
    "Miami": "flag_of_the_united_states",
    "Monaco": "flag_of_monaco",
    "Spain": "flag_of_spain",
    "Canada": "flag_of_canada",
    "Austria": "flag_of_austria",
    "United Kingdom": "united_kingdom",
    "Hungary": "flag_of_hungary",
    "Belgium": "flag_of_belgium",
    "Netherlands": "flag_of_the_netherlands",
    "Italy": "flag_of_italy",
    "Singapore": "flag_of_singapore",
    "Japan": "flag_of_japan",
    "United States": "flag_of_the_united_states",
    "Mexico": "flag_of_mexico",
    "Brazil": "flag_of_brazil",
    "Las Vegas": "flag_of_the_united_states",
    "Qatar": "flag_of_qatar",
    "United Arab Emirates": "flag_of_the_united_arab_emirates"
}

# Correspondencias GP
correspondencia_gp = {
    "Australian Grand Prix": "Australia",
    "Saudi Arabian Grand Prix": "Saudi Arabia",
    "Spanish Grand Prix": "Spain",
    "Azerbaijan Grand Prix": "Azerbaijan",
    "Bahrain Grand Prix": "Bahrain",
    "Monaco Grand Prix": "Monaco",
    "Canadian Grand Prix": "Canada",
    "Austrian Grand Prix": "Austria",
    "British Grand Prix": "United Kingdom",
    "Hungarian Grand Prix": "Hungary",
    "Belgian Grand Prix": "Belgium",
    "Dutch Grand Prix": "Netherlands",
    "Italian Grand Prix": "Italy",
    "Singapore Grand Prix": "Singapore",
    "Japanese Grand Prix": "Japan",
    "United States Grand Prix": "United States",
    "Mexican Grand Prix": "Mexico",
    "Brazilian Grand Prix": "Brazil",
    "Las Vegas Grand Prix": "United States",
    "Chinese Grand Prix": "China",
    "Miami Grand Prix": "United States",
    "Emilia Romagna Grand Prix": "Italy",
    "Mexico City Grand Prix": "Mexico",
    "Qatar Grand Prix": "Qatar",
    "Abu Dhabi Grand Prix": "United Arab Emirates",
    "São Paulo Grand Prix": "Brazil"
}

gp_names = [track['event'] for track in tracks]
constructor_puntos = {}

# Sumar puntos por constructor
for race in standings:
    race_name = race['race']
    for result in race['results']:
        driver = alias.get(result['driver'], result['driver'])
        team = result['team']
        puntos = result['points']
        if team not in constructor_puntos:
            constructor_puntos[team] = {gp: 0 for gp in gp_names}
        if race_name in constructor_puntos[team]:
            constructor_puntos[team][race_name] += puntos

# Máximos por GP
max_puntos_por_gp = {gp: 0 for gp in gp_names}
for team, puntos in constructor_puntos.items():
    for gp in gp_names:
        max_puntos_por_gp[gp] = max(max_puntos_por_gp[gp], puntos[gp])

# Máximo total
max_total = max(sum(p.values()) for p in constructor_puntos.values())

# Ordenar constructores por total
constructor_puntos_ordenados = sorted(constructor_puntos.items(), key=lambda item: sum(item[1].values()), reverse=True)

# Mapeo entre equipos y sus logos
logos_equipos = {
    "Red Bull Racing": "red-bull-racing-logo-1.jpg",
    "McLaren": "McLaren_Racing_logo.svg.png",
    "Kick Sauber": "kick_sauber-logo_brandlogos.net_qpgut-512x449.png",
    "Racing Bulls": "racing bulls.jpg",
    "Alpine": "Alpine_F1_Team_-_2022.svg.png",
    "Mercedes": "Mercedes-Benz_AMG_Petronas_Formula_One_Team_Logo_Wheelsology.JPG",
    "Aston Martin": "Aston.png",
    "Ferrari": "Ferrari_Logo.svg.png",
    "Williams": "williams-racing-logo-1.jpg",
    "Haas F1 Team": "Haas_F1_Team_Logo.svg.png"
}

# Generar HTML
html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Clasificación Mundial F1 2025 - CONSTRUCTORES</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            background-color: #000;
            color: #fff;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: start;
            height: 100vh;
            overflow: hidden;
        }
        h1 {
            color: white;
            font-size: 28px;
            margin: 10px 0;
        }
        h1 span {
            color: red;
        }
        .table-container {
            width: 95vw;
            height: 85vh;
            overflow: auto;
            background-color: #000;
            padding: 10px;
            box-sizing: border-box;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            background-color: white;
            color: black;
            font-size: 16px;
        }
        th, td {
            border: 1px solid #ccc;
            padding: 8px 10px;
            text-align: center;
        }
        th {
            background-color: #eee;
            position: sticky;
            top: 0;
            z-index: 2;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        img.flag {
            vertical-align: middle;
            margin-right: 6px;
            width: 16px;
            height: 12px;
        }
        .highlight {
            background-color: lightgreen;
        }
        .back-button {
            position: absolute;
            top: 10px;
            left: 10px;
            background-color: red;
            color: white;
            border: none;
            padding: 8px 12px;
            cursor: pointer;
            font-size: 16px;
        }
    </style>
</head>
<body>
    <button class="back-button" onclick="window.location.href='FORMINI.html'">&#8592; Volver</button>
    <h1>Clasificación Mundial F1 - Constructores <span>2025</span></h1>
    <div class="table-container">
        <table>
            <tr>
                <th>Equipo</th>
"""

# SECCIÓN CORREGIDA: Encabezados con logos GP
for gp in gp_names:
    # Usar correspondencia_gp para obtener el país del GP
    pais = correspondencia_gp.get(gp, "")
    bandera = banderas_gp.get(pais, None)
    
    if bandera:
        # Determinar extensión del archivo
        ext = ".svg"
        if bandera in ["united_kingdom"]:
            ext = ".png"
        
        html += f"<th><img class='flag' src='images/flags/{bandera}{ext}' width='20' height='15'><br>{gp}</th>"
    else:
        html += f"<th>{gp}</th>"

# Agregar columna de total
html += "<th>Total</th></tr>"

# Filas de equipos con logos
for equipo, puntos in constructor_puntos_ordenados:
    logo_filename = logos_equipos.get(equipo, "")
    ruta_logo = f"images/teams/{logo_filename}"
    html += f"<tr><td><img src='{ruta_logo}' width='60'><br>{equipo}</td>"

    total = 0
    for gp in gp_names:
        is_max = puntos[gp] == max_puntos_por_gp[gp] and puntos[gp] != 0
        class_attr = "class='highlight'" if is_max else ""
        html += f"<td {class_attr}>{puntos[gp]}</td>"
        total += puntos[gp]

    class_attr_total = "class='highlight'" if total == max_total else ""
    html += f"<td {class_attr_total}><b>{total}</b></td></tr>"

html += """
        </table>
    </div>
</body>
</html>
"""

# Guardar archivo
with open('clasis_constructores.html', 'w') as f:
    f.write(html)

print("✅ Tabla de constructores generada en 'clasis_constructores.html'")
