import fastf1
import pandas as pd
import json
import os

# Habilitar caché
fastf1.Cache.enable_cache('cache')

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

alias = {
    "Kimi Antonelli": "Andrea Kimi Antonelli"
}

lap_data = {}
drivers_set = set()

# Cargar datos
for gp_name, month, day, flag in races_2025:
    try:
        session = fastf1.get_session(2025, gp_name, 'R')
        session.load()

        if session.results.empty:
            continue

        laps = session.laps.pick_quicklaps()
        fastest_per_driver = laps.groupby('Driver')['LapTime'].min().reset_index()

        for _, row in fastest_per_driver.iterrows():
            driver_name = session.get_driver(row['Driver'])['FullName']
            lap_time = row['LapTime']
            driver_name = alias.get(driver_name, driver_name)

            if pd.notna(lap_time):
                total_seconds = lap_time.total_seconds()
                minutes, seconds = divmod(total_seconds, 60)
                formatted_time = f"{int(minutes):02d}:{seconds:06.3f}"
                lap_data.setdefault(driver_name, {})[gp_name] = formatted_time
                drivers_set.add(driver_name)
            else:
                print(f"{driver_name} no tiene vuelta rápida en {gp_name}")
    except Exception:
        pass

# Guardar JSON
os.makedirs("data", exist_ok=True)
with open("data/vueltas_rapidas_2025.json", "w", encoding="utf-8") as f:
    json.dump(lap_data, f, indent=4, ensure_ascii=False)

print("✅ Archivo JSON generado: data/vueltas_rapidas_2025.json")
