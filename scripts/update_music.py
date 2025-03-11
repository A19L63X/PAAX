import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def obtener_top_musica():
    url = 'https://www.elportaldemusica.es/lists'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    canciones = []
    for item in soup.select('.listElement'):
        try:
            cancion = {
                'titulo': item.select_one('.title a').get_text(strip=True),
                'artista': item.select_one('.artist a').get_text(strip=True),
                'portada': item.select_one('img')['src'],
                'streams': item.select_one('.count').get_text(strip=True)
            }
            canciones.append(cancion)
            if len(canciones) >= 100:
                break
        except Exception as e:
            print(f"Error procesando canción: {e}")
    
    return {
        'fecha_actualizacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'canciones': canciones
    }

if __name__ == '__main__':
    datos = obtener_top_musica()
    with open('top-musica.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
