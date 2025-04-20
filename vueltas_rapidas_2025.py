import pandas as pd
import json

# Cargar datos desde el archivo JSON creado
with open('data/vueltas_rapidas_2025.json', 'r') as f:
    lap_data = json.load(f)

# Lista de Grandes Premios 2025 con banderas
races_2025 = [
    ("Australia", 3, 16, "flag_of_australia.svg"),
    ("China", 3, 23, "flag_of_china.svg"),
    ("Japan", 4, 6, "flag_of_japan.svg"),
    ("Bahrain", 4, 13, "flag_of_bahrain.svg"),
    ("Saudi Arabia", 4, 20, "flag_of_saudi_arabia.svg"),
    ("Miami", 5, 4, "flag_of_the_united_states.svg"),
    ("Emilia Romagna", 5, 18, "flag_of_italy.svg"),
    ("Monaco", 5, 25, "flag_of_monaco.svg"),
    ("Spain", 6, 1, "flag_of_spain.svg"),
    ("Canada", 6, 15, "flag_of_canada.svg"),
    ("Austria", 6, 29, "flag_of_austria.svg"),
    ("Britain", 7, 6, "united_kingdom.png"),
    ("Belgium", 7, 27, "flag_of_belgium.svg"),
    ("Hungary", 8, 3, "flag_of_hungary.svg"),
    ("Netherlands", 8, 31, "flag_of_the_netherlands.svg"),
    ("Italy", 9, 7, "flag_of_italy.svg"),
    ("Azerbaijan", 9, 21, "flag_of_azerbaijan.svg"),
    ("Singapore", 10, 5, "flag_of_singapore.svg"),
    ("United States", 10, 19, "flag_of_the_united_states.svg"),
    ("Mexico", 10, 26, "flag_of_mexico.svg"),
    ("Brazil", 11, 9, "flag_of_brazil.svg"),
    ("Las Vegas", 11, 22, "flag_of_the_united_states.svg"),
    ("Qatar", 11, 30, "flag_of_qatar.svg"),
    ("Abu Dhabi", 12, 7, "flag_of_the_united_arab_emirates.svg")
]

# Alias de nombres
alias = {
    "Kimi Antonelli": "Andrea Kimi Antonelli"
}

# Banderas manuales para pilotos
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
    "Oliver Bearman": "united_kingdom"
}

drivers_set = set()

# Obtener pilotos desde el archivo JSON
drivers_list = sorted(lap_data.keys())

# Detectar mejores tiempos
best_times = {}
for gp_name, _, _, _ in races_2025:
    times = []
    for driver in drivers_list:
        time_str = lap_data.get(driver, {}).get(gp_name)
        if time_str and time_str != "-":
            minutes, sec = time_str.split(":")
            total_sec = int(minutes) * 60 + float(sec)
            times.append(total_sec)
    if times:
        best_times[gp_name] = min(times)

# Generar HTML
html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Mejores Vueltas Rápidas F1 2025  ⏱️</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #aaa; padding: 8px; text-align: center; }
        th { background-color: #444; color: white; }
        tr:nth-child(even) { background-color: #eee; }
        img { width: 25px; height: 15px; vertical-align: middle; }
        td:first-child { text-align: left; }
        .best-time { background-color: lightgreen; font-weight: bold; }
        .volver-btn {
            position: absolute;
            top: 20px;
            right: 20px;
            background-color: red;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            text-decoration: none;
            font-size: 14px;
        }
        .volver-btn:hover {
            background-color: darkred;
        }
    </style>
</head>
<body>
<a href="FORMINI.html" class="volver-btn">Volver</a>
<h2>Mejores Vueltas Rápidas de carrera F1 2025</h2>
<table>
    <tr>
        <th>Piloto</th>
"""

# Generar encabezados con banderas de los GP
for gp_name, _, _, flag in races_2025:
    html += f'<th><img src="images/flags/{flag}" alt="{gp_name}" title="{gp_name}"> {gp_name}</th>\n'

html += "</tr>\n"

# Mostrar pilotos con sus banderas y tiempos
for driver in drivers_list:
    piloto_flag = banderas_pilotos.get(driver, "united_kingdom")  # Default to UK flag if not found
    if piloto_flag == "united_kingdom":
        piloto_flag += ".png"
    else:
        piloto_flag += ".svg"

    html += f"<tr><td><img src='images/flags/{piloto_flag}' alt='{driver}' title='{driver}' style='width: 25px; height: 15px; vertical-align: middle;'> {driver}</td>"
    for gp_name, _, _, _ in races_2025:
        lap_time = lap_data.get(driver, {}).get(gp_name, "-")
        cell = f"{lap_time}"
        if lap_time != "-" and gp_name in best_times:
            minutes, sec = lap_time.split(":")
            total_sec = int(minutes) * 60 + float(sec)
            if abs(total_sec - best_times[gp_name]) < 0.001:
                cell = f'<span class="best-time">{lap_time}</span>'
        html += f"<td>{cell}</td>"
    html += "</tr>\n"

html += """
</table>
</body>
</html>
"""

with open("vueltas_rapidas_2025.html", "w", encoding="utf-8") as f:
    f.write(html)
