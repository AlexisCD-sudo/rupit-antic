import sqlite3
from sickle import Sickle

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
    # Taula auxiliar per guardar el punt d'aturada
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estat_extraccio (
            id INTEGER PRIMARY KEY,
            token TEXT
        )
    ''')
    conn.commit()
    conn.close()

def obtenir_ultim_token():
    conn = sqlite3.connect('rupit_antic.db')
    cursor = conn.cursor()
    cursor.execute('SELECT token FROM estat_extraccio WHERE id = 1')
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def guardar_token(token):
    conn = sqlite3.connect('rupit_antic.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO estat_extraccio (id, token) VALUES (1, ?)', (token,))
    conn.commit()
    conn.close()

def guardar_fotografia(foto):
    conn = sqlite3.connect('rupit_antic.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO fotografies (id, titol, creador, data, descripcio, url_orig, thumbnail)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', foto)
    conn.commit()
    conn.close()

def extreure_fotos_rupit():
    sickle = Sickle('https://mdc.csuc.cat/oai/oai.php')
    ultim_token = obtenir_ultim_token()
    
    try:
        if ultim_token:
            print(f" Reprenent l'extracció des de l'últim punt guardat...")
            records = sickle.ListRecords(resumptionToken=ultim_token)
        else:
            print(" Iniciant cerca des de zero a la Memòria Digital de Catalunya...")
            records = sickle.ListRecords(metadataPrefix='oai_dc')

        comptador = 0
        revisats = 0

        while True:
            try:
                record = next(records)
                revisats += 1
                
                meta = getattr(record, 'metadata', {})
                titol = meta.get('title', [''])[0] if meta.get('title') else ''
                desc = meta.get('description', [''])[0] if meta.get('description') else ''
                
                text_complet = f"{titol} {desc}".lower()
                
                if 'rupit' in text_complet or 'collsacabra' in text_complet:
                    identifiers = meta.get('identifier', [])
                    url_orig = identifiers[0] if identifiers else ""
                    
                    if "cdm/ref" in url_orig:
                        try:
                            parts = url_orig.split('/collection/')[1].split('/id/')
                            coll, img_id = parts[0], parts[1]
                            thumbnail = f"https://mdc.csuc.cat/digital/api/singleitem/image/{coll}/{img_id}/default.jpg"
                        except IndexError:
                            thumbnail = "https://via.placeholder.com/300x200?text=Imatge+Rupit"
                    else:
                        thumbnail = "https://via.placeholder.com/300x200?text=Arxiu+Rupit"

                    identifier = record.header.identifier
                    creador = meta.get('creator', ['Autor desconegut'])[0] if meta.get('creator') else 'Autor desconegut'
                    data = meta.get('date', ['Data desconeguda'])[0] if meta.get('date') else 'Data desconeguda'

                    guardar_fotografia((identifier, titol, creador, data, desc, url_orig, thumbnail))
                    comptador += 1
                    print(f" 📸 Trobat! ({comptador}): {titol[:50]}...")

                if revisats % 100 == 0:
                    # Guardem el token de continuació si existeix
                    if hasattr(records, 'resumption_token') and records.resumption_token:
                        guardar_token(records.resumption_token.token)
                    print(f"   Analitzats {revisats} registres... (Progrés desat)")

            except StopIteration:
                print("\n S'ha arribat al final de tot l'arxiu!")
                break

    except KeyboardInterrupt:
        print("\n Procés aturat per l'usuari. El punt d'aturada s'ha desat correctament.")
    except Exception as e:
        print(f"\n Error: {e}")

if __name__ == '__main__':
    inicialitzar_db()
    extreure_fotos_rupit()
