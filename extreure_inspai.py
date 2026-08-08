import sqlite3
import requests
from bs4 import BeautifulSoup
import urllib.parse

# Enllaç base de l'INSPAI
base_url = "https://www.inspai.cat/en/arxiu/1/24/cerca-d-imatges?text_filtre=Rupit&autor=&municipi=Rupit+i+Pruit&comarca=&fons=&drets=&anyIniciCerca=&anyFiCerca=&fotos_pagina=100&submit_recerca=CERCA"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, Gecko) Chrome/120.0.0.0 Safari/537.36'
}

conn = sqlite3.connect('rupit_antic.db')
c = conn.cursor()

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

noves_afegides = 0

print("Obrint cerca d'INSPAI...")
# Carreguem pàgina 1 i 2
for pag in [1, 2]:
    url = f"{base_url}&pag={pag}"
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        continue
        
    soup = BeautifulSoup(res.text, 'html.parser')
    
    # Cercar totes les imatges de la galeria de resultats
    imgs = soup.find_all('img')
    
    for img in imgs:
        src = img.get('src', '')
        # Filtrar imatges reals del catàleg (evitar icones del sistema)
        if 'imatges' in src or 'arxiu' in src or 'thumbs' in src or 'jpg' in src.lower() or 'jpeg' in src.lower():
            if 'logo' in src.lower() or 'icon' in src.lower():
                continue
                
            thumb_url = urllib.parse.urljoin("https://www.inspai.cat", src)
            
            # Busquem si la imatge té un enllaç pare
            parent_a = img.find_parent('a')
            if parent_a and parent_a.get('href'):
                page_url = urllib.parse.urljoin("https://www.inspai.cat", parent_a['href'])
            else:
                page_url = thumb_url

            titol = img.get('alt') or img.get('title') or "Fotografia de Rupit - INSPAI"
            if len(titol.strip()) < 3:
                titol = "Fotografia històrica de Rupit"

            foto_id = f"inspai_{hash(thumb_url)}"

            c.execute('''
                INSERT OR IGNORE INTO fotografies (id, titol, creador, data, descripcio, url_orig, thumbnail)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (foto_id, titol.strip(), "INSPAI - Diputació de Girona", "Històrica", "Fons fotogràfic INSPAI", page_url, thumb_url))

            if c.rowcount > 0:
                noves_afegides += 1

conn.commit()
print(f"Completat! S'han afegit {noves_afegides} noves fotografies a rupit_antic.db.")
conn.close()
