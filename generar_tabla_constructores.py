import json
from collections import defaultdict

# Cargar los datos de last_standings.json
with open('data/last_standings.json', 'r') as f:
    standings = json.load(f)

# Cargar los datos de tracks2025.json
with open('data/tracks2025.json', 'r') as f:
    tracks = json.load(f)

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
    "São Paulo Grand Prix": "Brazil"
}

# Obtener los nombres de los Grandes Premios
gp_names = [track['event'] for track in tracks]

# Diccionario para acumular puntos por equipo
equipos_puntos = defaultdict(lambda: {gp: 0 for gp in gp_names})

# Rellenar los puntos por equipo
for carrera in standings:
    gp = carrera['race']
    for resultado in carrera['results']:
        equipo = resultado['team']
        puntos = resultado['points']
        equipos_puntos[equipo][gp] += puntos

# Determinar máximos por GP y total
max_puntos_por_gp = {gp: 0 for gp in gp_names}
for puntos in equipos_puntos.values():
    for gp in gp_names:
        max_puntos_por_gp[gp] = max(max_puntos_por_gp[gp], puntos[gp])

max_total = max(sum(p.values()) for p in equipos_puntos.values())

# Ordenar equipos por total de puntos
equipos_ordenados = sorted(equipos_puntos.items(), key=lambda x: sum(x[1].values()), reverse=True)

# Iniciar HTML
html = """
<<!DOCTYPE html>
<html>
<head>
    <meta charset=\"UTF-8\">
    <title>Clasificación Mundial F1 2025 - EQUIPOS</title>
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
    <button class=\"back-button\" onclick=\"window.location.href='formini.html'\">&#8592; Volver</button>
    <h1>Clasificación Mundial F1 - Equipos <span>2025</span></h1>
    <div class=\"table-container\">
        <table>
            <tr>
                <th>Equipo</th>
"""

# Agregar encabezados con banderas
to_html = html
for gp in gp_names:
    pais = correspondencia_gp.get(gp)
    if pais and pais in banderas_gp:
        bandera = banderas_gp[pais]
        ext = ".png" if bandera == "united_kingdom" else ".svg"
        to_html += f"<th><img class='flag' src='images/flags/{bandera}{ext}'><br>{gp}</th>"
    else:
        to_html += f"<th>{gp}</th>"

to_html += "<th>Total</th>"

# Agregar filas por equipo
for equipo, puntos in equipos_ordenados:
    to_html += f"<tr><td>{equipo}</td>"
    total = 0
    for gp in gp_names:
        val = puntos[gp]
        total += val
        clase = "highlight" if val == max_puntos_por_gp[gp] and val != 0 else ""
        to_html += f"<td class='{clase}'>{val}</td>"
    clase_total = "highlight" if total == max_total else ""
    to_html += f"<td class='{clase_total}'><b>{total}</b></td></tr>"

to_html += """
        </table>
    </div>
</body>
</html>
"""

# Guardar archivo HTML
with open('clasis_equipos.html', 'w') as f:
    f.write(to_html)

print("✅ Tabla de clasificación de equipos generada correctamente en 'clasis_equipos.html'")