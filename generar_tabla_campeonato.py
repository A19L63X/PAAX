
# -*- coding: utf-8 -*-
import json

# Cargar los datos de last_standings.json
with open('data/last_standings.json', 'r') as f:
    standings = json.load(f)

# Cargar los datos de tracks2025.json
with open('data/tracks2025.json', 'r') as f:
    tracks = json.load(f)

# Diccionario de alias para los pilotos
alias = {
    "Kimi Antonelli": "Andrea Kimi Antonelli",
    # Puedes agregar más alias si aparecen errores similares en el futuro
}

# Diccionario de banderas de los países de los pilotos
banderas_pilotos = {
    "Max Verstappen": "flag_of_the_netherlands",
    "Lando Norris": "united_kingdom",
    "Gabriel Bortoleto": "flag_of_brazil",
    "Isack Hadjar": "flag_of_france",
    "Jack Doohan": "flag_of_australia",
    "Pierre Gasly": "flag_of_france",
    "Andrea Kimi Antonelli": "flag_of_italy",
    "Fernando Alonso": "flag_of_spain",
    "Charles Leclerc": "flag_of_monaco",
    "Lance Stroll": "flag_of_canada",
    "Liam Lawson": "flag_of_new_zealand",
    "Alexander Albon": "flag_of_thailand",
    "Nico Hulkenberg": "flag_of_germany",
    "Yuki Tsunoda": "flag_of_japan",
    "Esteban Ocon": "flag_of_france",
    "Lewis Hamilton": "united_kingdom",
    "Carlos Sainz": "flag_of_spain",
    "George Russell": "united_kingdom",
    "Oscar Piastri": "flag_of_australia",
    "Oliver Bearman": "united_kingdom",  
    "Franco Colapinto": "flag_of_argentina"
}

# Diccionario de banderas de los países de los Grandes Premios
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

# Obtener los nombres de los Grandes Premios desde tracks2025.json
gp_names = [track['event'] for track in tracks]

# Inicializar un diccionario para acumular puntos por piloto
piloto_puntos = {}

# Llenar la tabla con los puntos de los pilotos
for race in standings:
    race_name = race['race']
    for result in race['results']:
        piloto = alias.get(result['driver'], result['driver'])  # Normaliza el nombre
        puntos = result['points']
        if piloto not in piloto_puntos:
            piloto_puntos[piloto] = {gp: 0 for gp in gp_names}
        if race_name in piloto_puntos[piloto]:
            piloto_puntos[piloto][race_name] += puntos

# Determinar la mayor puntuación de cada carrera (incluyendo la columna total)
max_puntos_por_gp = {gp: 0 for gp in gp_names}
for piloto, puntos in piloto_puntos.items():
    for gp in gp_names:
        max_puntos_por_gp[gp] = max(max_puntos_por_gp[gp], puntos[gp])

# Encontrar la mayor puntuación total
max_total = max(sum(puntos.values()) for puntos in piloto_puntos.values())

# Ordenar los pilotos por la columna total de mayor a menor
piloto_puntos_ordenados = sorted(piloto_puntos.items(), key=lambda item: sum(item[1].values()), reverse=True)

# Comenzar a construir el HTML con los colores
html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Clasificación Mundial F1 2025 - PILOTOS</title>
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
    <h1>Clasificación Mundial F1 - Pilotos <span>2025</span></h1>
    <div class="table-container">
        <table>          <tr>
                <th>Piloto</th>
"""

# Continuar con el resto de código como está...


# Diccionario de correspondencias entre nombres completos de GP y países
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
"Chinese Grand Prix": "China",
"São Paulo Grand Prix": "Brazil"
}

# Agregar los encabezados de las columnas (carreras con banderas)
for gp in gp_names:
    # Buscar el nombre del GP en el diccionario de correspondencias
    normalized_gp_name = correspondencia_gp.get(gp, None)
    
    if normalized_gp_name:
        # Si encontramos una correspondencia, obtenemos la bandera
        bandera_gp = banderas_gp.get(normalized_gp_name, None)
        if bandera_gp:  # Solo asignamos la bandera si se encuentra en el diccionario
            extension = ".png" if bandera_gp == "united_kingdom" else ".svg"
            html += f"<th><img class='flag' src='images/flags/{bandera_gp}{extension}' width='20' height='15'><br>{gp}</th>"
        else:
            # Si no hay bandera para el GP, mostramos una celda sin imagen
            html += f"<th>{gp}</th>"
    else:
        # Si no hay correspondencia, mostramos el GP sin bandera
        html += f"<th>{gp}</th>"

# Agregar la columna Total
html += "<th>Total</th>"

# Generar filas de la tabla con los colores de puntuación
for piloto, puntos in piloto_puntos_ordenados:
    bandera_piloto = banderas_pilotos.get(piloto, "default")
    extension = ".png" if bandera_piloto == "united_kingdom" else ".svg"
    ruta_bandera = f"images/flags/{bandera_piloto}{extension}"
    html += f"<tr><td><img class='flag' src='{ruta_bandera}' width='20' height='15'> {piloto}</td>"

    total = 0
    for gp in gp_names:
        is_max = puntos[gp] == max_puntos_por_gp[gp] and puntos[gp] != 0  # Verifica si la puntuación es la máxima y no es cero
        class_attr = "class='highlight'" if is_max else ""
        html += f"<td {class_attr}>{puntos[gp]}</td>"
        total += puntos[gp]
    
    # Resaltar la columna total si es la máxima
    class_attr_total = "class='highlight'" if total == max_total else ""
    html += f"<td {class_attr_total}><b>{total}</b></td></tr>"

html += """
    </table>
</div>
</body>
</html>
"""

# Guardar el archivo HTML
with open('clasis.html', 'w') as f:
    f.write(html)

print("✅ La tabla ha sido generada correctamente en 'clasis.html'")
