import os
import json
import fastf1
from datetime import datetime

def get_reliable_standings():
    """Obtiene clasificaciones usando calendario 2025"""
    os.makedirs('cache', exist_ok=True)
    fastf1.Cache.enable_cache('cache')
    fastf1.set_log_level('ERROR')

    YEAR = 2025
    CACHE_FILE = 'data/last_standings.json'
    all_results = []
    today = datetime.now().date()
    
    # Cargar calendario 2025
    try:
        with open('data/tracks2025.json', 'r') as f:
            tracks = json.load(f)
        # Filtrar solo carreras pasadas
        past_events = [
            t for t in tracks 
            if datetime.strptime(t['date'], '%Y-%m-%d').date() <= today
        ]
        print(f"✅ Calendario 2025 cargado: {len(past_events)} carreras disputadas")
    except Exception as e:
        print(f"⚠️ Error cargando calendario: {str(e)}")
        past_events = []

    try:
        # Procesar solo carreras ya realizadas
        for i, event in enumerate(past_events, 1):
            round_num = event['round']
            official_name = event['event']
            print(f"\n🏁 Procesando ronda {round_num}: {official_name}")
            
            try:
                # Obtener datos de FastF1 usando número de ronda
                race = fastf1.get_session(YEAR, round_num, 'R')
                race.load(telemetry=False, weather=False)
                
                if race.results.empty:
                    print(f"⏭️ Sin resultados, saltando...")
                    continue
                
                # Recolectar resultados
                results = []
                for _, row in race.results.iterrows():
                    results.append({
                        'position': int(row['Position']),
                        'driver': row['FullName'],
                        'team': row['TeamName'],
                        'points': int(row['Points'])
                    })
                
                all_results.append({
                    'race': official_name,  # Nombre oficial del calendario
                    'date': str(race.date),
                    'results': results
                })
                print(f"✅ Resultados: {len(results)} pilotos")
                
            except Exception as e:
                print(f"⚠️ Error en ronda {round_num}: {str(e)}")
                continue

        # Guardar JSON
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        with open(CACHE_FILE, 'w') as f:
            json.dump(all_results, f, indent=2)
        print(f"\n💾 Datos guardados en: {CACHE_FILE}")
        return all_results

    except Exception as e:
        print(f"\n❌ Error general: {str(e)}")
        # Cargar respaldo si existe
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE) as f:
                    return json.load(f)
            except:
                return None

if __name__ == "__main__":
    print("="*50)
    print(f"🏎️  ACTUALIZANDO CLASIFICACIONES F1 2025")
    print("="*50)
    data = get_reliable_standings()
    
    if data:
        print("\n🏆 CARRERAS PROCESADAS:")
        for i, race in enumerate(data, 1):
            print(f"{i}. {race['race']} - {len(race['results'])} pilotos")
        print("\n✅ Proceso completado!")
    else:
        print("\n❌ Error: No se pudieron obtener datos")