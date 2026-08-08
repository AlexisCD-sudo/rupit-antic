import sqlite3
import os
from bs4 import BeautifulSoup
import urllib.parse

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

noves = 0

# Fitxers HTML desats des del navegador
fitxers = ['inspai.html', 'inspai2.html']

for fitxer in fitxers:
    if not os.path.exists(fitxer):
        continue
        
    print(f"Processant {fitxer}...")
    with open(fitxer, 'r', encoding='utf-8', errors='ignore') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Busquem tots els enllaços o imatges de la cerca
    imgs = soup.find_all('img')
    
    for img in imgs:
        src = img.get('src', '')
        
        # Filtrar imatges reals del catàleg
        if any(term in src.lower() for term in ['arxiu', 'imatge', 'thumb', 'jpg', 'jpeg']):
            if any(b in src.lower() for b in ['logo', 'icon', 'head', 'foot', 'btn', 'button']):
                continue

            thumb_url = urllib.parse.urljoin("https://www.inspai.cat", src)
            
            parent_a = img.find_parent('a')
            if parent_a and parent_a.get('href'):
                page_url = urllib.parse.urljoin("https://www.inspai.cat", parent_a['href'])
            else:
                page_url = thumb_url

            titol = img.get('alt') or img.get('title') or (parent_a.get('title') if parent_a else "Fotografia de Rupit - INSPAI")
            if not titol or len(titol.strip()) < 3:
                titol = "Fotografia de Rupit - INSPAI"

            foto_id = f"inspai_{abs(hash(thumb_url))}"

            c.execute('''
                INSERT OR IGNORE INTO fotografies (id, titol, creador, data, descripcio, url_orig, thumbnail)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (foto_id, titol.strip(), "INSPAI - Diputació de Girona", "Històrica", "Fons fotogràfic INSPAI", page_url, thumb_url))

            if c.rowcount > 0:
                noves += 1

conn.commit()
print(f"\nFinalitzat! S'han afegit {noves} noves fotografies a rupit_antic.db.")
conn.close()
