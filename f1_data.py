import os
import json
import fastf1
from datetime import datetime

def get_reliable_standings():
    """Obtiene clasificaciones con múltiples fuentes de respaldo"""
    fastf1.Cache.enable_cache('cache')
    fastf1.set_log_level('ERROR')  # Solo muestra errores críticos


    YEAR = 2025
    CACHE_FILE = 'data/last_standings.json'

    try:
        print(f"Cargando calendario {YEAR}...")
        schedule = fastf1.get_event_schedule(YEAR)
    except Exception:
        print(f"No se pudo cargar {YEAR}. Intentando con otro año...")
        return None

    try:
        valid_races = [event for event in schedule['EventName'] 
                      if 'Grand Prix' in event and not 'Test' in event]
        
        if not valid_races:
            raise ValueError("No se encontraron carreras válidas")

        all_results = []

        for race_name in valid_races:
            print(f"\nObteniendo datos de {race_name}...")
            race = fastf1.get_session(YEAR, race_name, 'R')
            race.load(telemetry=False, weather=False, messages=False)

            if race.results.empty:
                print(f"Sin resultados para {race_name}. Saltando...")
                continue

            results = []
            for _, row in race.results.iterrows():
                driver = row['Driver']
                original_country = driver.country
                
                
                results.append({
                    'position': int(row['Position']),
                    'driver': row['FullName'],
                    'team': row['TeamName'],
                    'points': int(row['Points']),
                })

            all_results.append({
                'race': race.event['EventName'],
                'date': str(race.event['Session5Date']),
                'results': sorted(results, key=lambda x: x['position'])
            })

        os.makedirs('data', exist_ok=True)
        with open(CACHE_FILE, 'w') as f:
            json.dump(all_results, f, indent=2)

        return all_results

    except Exception as e:
        print(f"\nError crítico: {str(e)}")
        
        if os.path.exists(CACHE_FILE):
            print("Cargando datos cacheados locales...")
            with open(CACHE_FILE) as f:
                return json.load(f)
        
        return None

def generate_html(data):
    """Genera un archivo HTML para mostrar los resultados de todas las carreras"""
    html_content = f"""
    <html>
    <head>
        <title>Clasificación F1 - {data[0]['race']}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            table, th, td {{ border: 1px solid black; }}
            th, td {{ padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            h1 {{ color: #333; }}
            img.flag {{ height: 20px; vertical-align: middle; margin-right: 5px; }}
        </style>
    </head>
    <body>
        <h1>Clasificación F1 - Temporada 2025</h1>
    """

    for season_data in data:
        html_content += f"""
        <h2>{season_data['race']}</h2>
        <h4>Fecha: {season_data['date']}</h4>
        <table>
            <tr>
                <th>Posición</th>
                <th>Piloto</th>
                <th>Equipo</th>
                <th>Puntos</th>
            </tr>
        """

        for driver in season_data['results']:
            html_content += f"""
            <tr>
                <td>{driver['position']}</td>
                <td>{driver['driver']}</td>
                <td>{driver['team']}</td>
                <td>{driver['points']}</td>
            </tr>
            """

        html_content += """
        </table>
        """

    html_content += """
    </body>
    </html>
    """
    
    with open('clasis.html', 'w') as f:
        f.write(html_content)
    print("\n✅ El archivo HTML se ha guardado como 'clasis.html'")

if __name__ == "__main__":
    data = get_reliable_standings()
    
    if data:
        print(f"\n🏁 Clasificación Final - Temporada 2025 🏁")
        
        for season_data in data:
            print(f"\nGran Premio: {season_data['race']}")
            print(f"Fecha: {season_data['date']}")
            for driver in season_data['results']:
                print(f"{driver['position']:>2}. {driver['driver']:<20} {driver['team']:<15} {driver['points']} pts")
        
        generate_html(data)
    else:
        print("\n❌ No se pudieron obtener datos. Soluciones:")
        print("1. Ejecuta: rm -rf f1_cache/")
        print("2. Verifica tu conexión a internet")
        print("3. Prueba con python3 -m pip install --upgrade fastf1")