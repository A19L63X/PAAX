import requests
from bs4 import BeautifulSoup
import json
import os
import re
from datetime import datetime

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
}

urls = [
    "https://es.motorsport.com/f1/results/2025/gp-de-china-653027/?st=SPR"
]

output_base_dir = os.path.dirname(os.path.abspath(__file__))  # Ruta del script
sprint_output_dir = os.path.join(output_base_dir, "Sprint")
os.makedirs(sprint_output_dir, exist_ok=True)

def extraer_piloto(columna):
    """Extrae el nombre del piloto de la columna combinada"""
    # Eliminar texto del equipo si existe
    piloto_text = columna.get_text(strip=True)
    for equipo in ['Ferrari', 'Mercedes', 'Red Bull', 'McLaren', 'Aston Martin']:
        piloto_text = piloto_text.replace(equipo, '')
    return piloto_text.strip()

def procesar_nombre_piloto(nombre_completo):
    """Separa el nombre y apellido del piloto"""
    if not nombre_completo:
        return {"Nombre": "", "Apellido": ""}
    
    partes = nombre_completo.split('.') if '.' in nombre_completo else nombre_completo.split()
    if len(partes) >= 2:
        return {
            "Nombre": partes[0].strip(),
            "Apellido": ' '.join(partes[1:]).strip()
        }
    return {
        "Nombre": "",
        "Apellido": nombre_completo.strip()
    }

for url in urls:
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extraer el nombre del GP de la URL
        match = re.search(r'gp-de-([a-z\-]+)', url)
        if match:
            nombre_gp_url = match.group(1).replace('-', ' ').title()
            nombre_archivo_base = match.group(1).replace('-', ' ').title().replace(' ', '')
            nombre_archivo_json = f"Sp_{nombre_archivo_base}.json"
        else:
            nombre_gp_url = "Gran Premio Desconocido"
            nombre_archivo_json = "Sp_Desconocido.json"

        # Encontrar la tabla de resultados
        parrilla = soup.find('table', {'class': 'ms-table'})
        if not parrilla:
            print(f"No se encontró la tabla en {url}")
            continue

        # Obtener todas las filas de la tabla
        filas = parrilla.find_all('tr')
        if len(filas) < 2:  # Encabezado + al menos una fila de datos
            print(f"Tabla sin datos en {url}")
            continue

        # Procesar encabezados (si existen)
        encabezados = []
        if filas[0].find('th'):
            encabezados = [th.get_text(strip=True) for th in filas[0].find_all('th') if th.get_text(strip=True)]

        # Si no hay encabezados válidos, usar los predeterminados
        if not encabezados:
            encabezados = [
                "Pos", "Piloto", "Número", "Bandera", "Equipo", "Motor", 
                "Tiempo", "Diferencia", "Velocidad Máx", "Puntos", 
                "Vueltas", "Equipo", "Motor"
            ]

        resultados = []
        for fila in filas[1:]:  # Saltamos la fila de encabezados
            columnas = fila.find_all('td')
            if not columnas:
                continue

            # Crear diccionario con los datos
            datos_fila = {
                "Posición": columnas[0].get_text(strip=True) if len(columnas) > 0 else "",
                "Número": columnas[2].get_text(strip=True) if len(columnas) > 2 else "",
                "Piloto": extraer_piloto(columnas[1]) if len(columnas) > 1 else "",
                "Equipo": columnas[4].get_text(strip=True) if len(columnas) > 4 else "",
                "Motor": columnas[5].get_text(strip=True) if len(columnas) > 5 else "",
                "Tiempo": columnas[6].get_text(strip=True) if len(columnas) > 6 else "",
                "Diferencia": columnas[7].get_text(strip=True) if len(columnas) > 7 else "",
                "Velocidad Máx": columnas[8].get_text(strip=True) if len(columnas) > 8 else "",
                "Puntos": columnas[9].get_text(strip=True) if len(columnas) > 9 else "",
                "Vueltas": columnas[10].get_text(strip=True) if len(columnas) > 10 else ""
            }

            # Añadir datos procesados del piloto
            datos_piloto = procesar_nombre_piloto(datos_fila["Piloto"])
            datos_fila.update(datos_piloto)

            resultados.append(datos_fila)

        # Crear el objeto de datos completo
        datos_gp = {
            "Nombre": f"Gran Premio de {nombre_gp_url} (Sprint)",
            "URL": url,
            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Resultados": resultados
        }

        # Guardar en archivo JSON
        filename = os.path.join(sprint_output_dir, nombre_archivo_json)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(datos_gp, f, ensure_ascii=False, indent=4)

        print(f"✅ Datos de la carrera al sprint guardados correctamente en {filename}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión al procesar {url}: {e}")
    except Exception as e:
        print(f"❌ Error inesperado al procesar {url}: {e}")