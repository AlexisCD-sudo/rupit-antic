import sqlite3
import re
from sickle import Sickle

# Endpoint OAI de la Memòria Digital de Catalunya i altres fons
ENDPOINTS = [
    {
        'nom': 'MDC / CRDI / INSPAI',
        'url': 'https://mdc.csuc.cat/oai/oai.php',
        'prefix': 'oai_dc'
    },
    {
        'nom': 'Calaix (Patrimoni Arquitectònic / Gencat)',
        'url': 'https://calaix.gencat.cat/oai/request',
        'prefix': 'oai_dc'
    }
]

def inicialitzar_db():
    conn = sqlite3.connect('rupit_antic.db')
    cursor = conn.cursor()
    cursor.execute('''
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
    conn.commit()
    conn.close()

def extreure_any(text_data):
    """Detecta qualsevol any de 4 xifres dins del text de la data."""
    if not text_data:
        return None
    coincidencies = re.findall(r'\b(1[789]\d\d)\b', str(text_data))
    if coincidencies:
        return int(coincidencies[0])
    return None

def guardar_fotografia(foto):
    conn = sqlite3.connect('rupit_antic.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO fotografies (id, titol, creador, data, descripcio, url_orig, thumbnail)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', foto)
    conn.commit()
    conn.close()

def extreure_fotos_multiarxiu():
    inicialitzar_db()
    
    # Paraules clau de cerca territorial
    termes_cerca = ['rupit', 'pruit', 'collsacabra', 'sallent de rupit', 'sant joan de fabregues']
    
    total_trobades = 0

    for fons in ENDPOINTS:
        print(f"\n Connectant amb l'arxiu: {fons['nom']}...")
        try:
            sickle = Sickle(fons['url'])
            records = sickle.ListRecords(metadataPrefix=fons['prefix'])
            
            revisats = 0
            trobades_fons = 0

            for record in records:
                revisats += 1
                meta = getattr(record, 'metadata', {})
                
                titol = meta.get('title', [''])[0] if meta.get('title') else ''
                desc = meta.get('description', [''])[0] if meta.get('description') else ''
                text_complet = f"{titol} {desc}".lower()
                
                # Check 1: Coincidència de territori
                if any(terme in text_complet for terme in termes_cerca):
                    
                    # Check 2: Filtre d'any (<= 1960)
                    dates = meta.get('date', [''])
                    str_data = dates[0] if dates else 'Data no consta'
                    any_foto = extreure_any(str_data)
                    
                    if any_foto and any_foto > 1960:
                        continue # Descartem les posteriors a 1960
                    
                    # Check 3: Identificar URLs d'imatge
                    identifiers = meta.get('identifier', [])
                    url_orig = ""
                    thumbnail = ""
                    
                    for ident in identifiers:
                        if "http" in ident:
                            url_orig = ident
                            break
                    
                    # Generació de miniatura segons la font
                    if "cdm/ref" in url_orig:
                        try:
                            parts = url_orig.split('/collection/')[1].split('/id/')
                            coll, img_id = parts[0], parts[1]
                            thumbnail = f"https://mdc.csuc.cat/digital/api/singleitem/image/{coll}/{img_id}/default.jpg"
                        except IndexError:
                            continue
                    elif "calaix.gencat.cat" in url_orig:
                        thumbnail = url_orig # Miniatura d'INVARQUIT / Calaix
                    else:
                        # Si no té enllaç directe d'imatge vàlid, la saltem
                        continue

                    identifier = record.header.identifier
                    creador = meta.get('creator', ['Autor desconegut'])[0] if meta.get('creator') else 'Autor desconegut'

                    # Guardar a la base de dades
                    guardar_fotografia((identifier, titol, creador, str_data, desc, url_orig, thumbnail))
                    trobades_fons += 1
                    total_trobades += 1
                    
                    any_mostrat = any_foto if any_foto else "Antiga (s/d)"
                    print(f"  📸 [{any_mostrat}] {titol[:50]}...")

                if revisats % 300 == 0:
                    print(f"    Analitzats {revisats} registres de {fons['nom']}...")

        except Exception as e:
            print(f" ⚠️ Error en consultar {fons['nom']}: {e}")

    print(f"\n Procs d'extracció finalitzat! S'han afegit {total_trobades} fotografies històriques.")

if __name__ == '__main__':
    extreure_fotos_multiarxiu()
