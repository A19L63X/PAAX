import requests
from bs4 import BeautifulSoup
import json
import os
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
}

urls = [
    "https://lat.motorsport.com/f1/results/2025/gp-de-bahrein-653347/?st=GRID",
    "https://lat.motorsport.com/f1/results/2025/gp-de-japon-653030/?st=GRID",
    "https://lat.motorsport.com/f1/results/2025/gp-de-china-653027/?st=GRID",
    "https://lat.motorsport.com/f1/results/2025/gp-de-australia-653024/?st=GRID",
    "https://lat.motorsport.com/f1/results/2025/gp-de-arabia-saudi/?st=GRID",
    "https://es.motorsport.com/f1/results/2025/gp-de-miami-653353/?st=GRID",
    "https://es.motorsport.com/f1/results/2025/gp-emilia-romagna-653356/?st=GRID",
    "https://es.motorsport.com/f1/results/2025/gp-de-monaco-653359/?st=GRID",
    "https://es.motorsport.com/f1/results/2025/gp-de-espana-653362/?st=GRID",
    "https://es.motorsport.com/f1/results/2025/gp-de-canada-653365/?st=GRID",
    "https://es.motorsport.com/f1/results/2025/gp-de-austria-653368/?st=GRID",
    "https://es.motorsport.com/f1/results/2025/gp-de-gran-bretana-653371/?st=GRID",
    "https://es.motorsport.com/f1/results/2025/gp-de-belgica-653374/?st=GRID",
    "https://es.motorsport.com/f1/results/2025/gp-de-hungria-653377/?st=GRID",
    "https://es.motorsport.com/f1/results/2025/gp-paises-bajos-653380/?st=GRID",
    "https://es.motorsport.com/f1/results/2025/gp-de-italia-653383/?st=GRID",
    "https://es.motorsport.com/f1/results/2025/gp-de-azerbaiyan-653386/?st=GRID",
    "https://es.motorsport.com/f1/results/2025/gp-de-singapur-653389/?st=GRID"
]

import os

# Ruta relativa al script (elimina la ruta absoluta)
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Qualy")
os.makedirs(output_dir, exist_ok=True)

for url in urls:
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraer el nombre del GP de la URL
        match = re.search(r'gp-(?:de-)?([a-z\-]+)', url)
        if match:
            nombre_gp_url = match.group(1).replace('-', ' ').title()
            nombre_archivo = match.group(1).replace('-', ' ').title().replace(' ', '')
        else:
            # Intentar extraer directamente del título de la página
            title_element = soup.find('title')
            if title_element and 'GP' in title_element.text:
                title_text = title_element.text
                gp_name = re.search(r'GP\s+(?:de\s+)?([A-Za-z\s]+)', title_text)
                if gp_name:
                    nombre_gp_url = gp_name.group(1).strip()
                    nombre_archivo = nombre_gp_url.replace(' ', '')
                else:
                    nombre_gp_url = "Gran Premio Desconocido"
                    nombre_archivo = "GP_Desconocido"
            else:
                nombre_gp_url = "Gran Premio Desconocido"
                nombre_archivo = "GP_Desconocido"
        
        # Encontrar la tabla de resultados
        parrilla = soup.find('table', {'class': 'ms-table'})
        if not parrilla:
            print(f"No se encontró la tabla en {url}")
            continue
        
        # Obtener los encabezados de la tabla
        encabezados = []
        headers_row = parrilla.find('tr')
        if headers_row:
            for th in headers_row.find_all('th'):
                encabezado = th.get_text(strip=True)
                if encabezado:  # Solo añadir si no está vacío
                    encabezados.append(encabezado)
        
        # Si no hay encabezados o no son suficientes, usar los estándar
        if not encabezados or len(encabezados) < 3:
            encabezados = ["Pos", "Piloto/Equipo", "No", "Nac", "Equipo", "Motor", "Tiempo", "Gap", "Vel. máx."]
        
        resultados = []
        for fila in parrilla.find_all('tr')[1:]:  # Saltamos la fila de encabezados
            columnas = fila.find_all('td')
            if not columnas:
                continue
                
            # Crear un diccionario para esta fila
            datos_fila = {}
            
            # Extraer todos los datos de cada columna
            for i, columna in enumerate(columnas):
                # Asegurarse de que tenemos un encabezado para esta columna
                if i < len(encabezados):
                    clave = encabezados[i]
                else:
                    clave = f"Columna_{i}"
                
                # Obtener el texto completo de la columna
                valor = columna.get_text(strip=True)
                datos_fila[clave] = valor
            
            resultados.append(datos_fila)
        
        # Crear el objeto de datos completo
        datos_gp = {
            "Nombre": f"Gran Premio de {nombre_gp_url}",
            "URL": url,
            "Resultados": resultados
        }
        
        # Guardar en archivo JSON
        filename = os.path.join(output_dir, f"Q_{nombre_archivo}.json")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(datos_gp, f, ensure_ascii=False, indent=4)
            
        print(f"✅ Datos guardados correctamente en {filename}")
        
    except Exception as e:
        print(f"❌ Error procesando {url}: {e}")
