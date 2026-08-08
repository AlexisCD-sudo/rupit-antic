import sys
import sqlite3
import requests
from bs4 import BeautifulSoup
import urllib.parse

# La URL la passarem com a paràmetre o la posarem directament
if len(sys.argv) > 1:
    target_url = sys.argv[1]
else:
    print("Si us plau, passa la URL com a paràmetre. Ex: python3 extreure_enllac.py 'https://...'")
    sys.exit(1)

print(f"Iniciant extracció des de l'enllaç filtrat...")

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, Gecko) Chrome/120.0.0.0 Safari/537.36'
}

conn = sqlite3.connect('rupit_antic.db')
c = conn.cursor()

# Assegurem la taula
c.execute('''
    CREATE TABLE IF NOT EXISTS fotografies (
        id TEXT PRIMARY KEY,
        titol TEXT,
        creador TEXT,
        data TEXT,
        descripcio TEXT,
        url_orig TEXT,
        thumbnail TEXT
    )
''')

 afegides = 0

def processar_pagina(url):
    global afegides
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error en carregar la pàgina: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Adaptació automàtica segons el repositori (MDC / DSpace / Calaix / Arxius en línia)
    items = soup.select('.artifact-description, .item-result, .search-result, .thumbnail, tr.ds-table-row')
    
    if not items:
        # Cercador genèric d'imatges/enllaços si no troba estructures estàndard
        items = soup.find_all('a', href=True)

    print(f"S'han localitzat potencials elements a la pàgina.")

    for idx, item in enumerate(items):
        try:
            # Extracció genèrica d'enllaç, títol i miniatura
            link_tag = item.find('a') if item.name != 'a' else item
            if not link_tag or not link_tag.get('href'):
                continue
                
            link = urllib.parse.urljoin(url, link_tag['href'])
            titol = link_tag.get_text(strip=True) or "Fotografia de Rupit"
            
            img_tag = item.find('img')
            thumb = urllib.parse.urljoin(url, img_tag['src']) if img_tag and img_tag.get('src') else link
            
            # ID únic basat en la URL
            foto_id = f"dir_{hash(link)}"

            c.execute('''
                INSERT OR IGNORE INTO fotografies (id, titol, creador, data, descripcio, url_orig, thumbnail)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (foto_id, titol, "Arxiu Digital", "Desconeguda", "", link, thumb))
            
            if c.rowcount > 0:
                afegides += 1

        except Exception as e:
            continue

    conn.commit()

# Executem sobre la URL principal
processar_pagina(target_url)

print(f"\nProceś completat! S'han afegit {afegides} noves fotografies a la base de dades.")
conn.close()
