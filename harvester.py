import sqlite3
import re
import json
import os
from sickle import Sickle

# Endpoints OAI-PMH
# Llista completa de servidors OAI-PMH i fons documentals sol·licitats
ENDPOINTS = [
    {
        'nom': 'MDC (Memòria Digital de Catalunya - inclou fons comarcals i universitaris)',
        'url': 'https://mdc.csuc.cat/oai/oai.php',
        'prefix': 'oai_dc'
    },
    {
        'nom': 'Calaix / INVARQUIT (Patrimoni Arquitectònic Gencat)',
        'url': 'https://calaix.gencat.cat/oai/request',
        'prefix': 'oai_dc'
    },
    {
        'nom': 'CRDI Girona / INSPAI (Diputació de Girona)',
        'url': 'https://www me.girona.cat/oai/oai.php', # Connector centralitzat de fons gironins
        'prefix': 'oai_dc'
    },
    {
        'nom': 'Arxiu Fotogràfic de Barcelona (AFB / Arxius Municipals BCN)',
        'url': 'https://arxiuhistoric.bcn.cat/oai/request',
        'prefix': 'oai_dc'
    },
    {
        'nom': 'Arxius en Línia Gencat (Arxiu Comarcal d Osona, Garrotxa, Alt Penedès)',
        'url': 'https://arxiusenlinia.cultura.gencat.cat/oai/request',
        'prefix': 'oai_dc'
    }
]
FITXER_ESTAT = 'estat_cerca.json'

def carregar_estat():
    """Carrega el punt on es va quedar la darrera cerca."""
    if os.path.exists(FITXER_ESTAT):
        try:
            with open(FITXER_ESTAT, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def desar_estat(fons_nom, token):
    """Desa el token de resum actual per reprendre-ho després."""
    estat = carregar_estat()
    estat[fons_nom] = token
    with open(FITXER_ESTAT, 'w') as f:
        json.dump(estat, f, indent=2)

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
    if not text_data:
        return None
    coincidencies = re.findall(r'\b(1[89]\d\d)\b', str(text_data))
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

def extreure_fotos_amb_pau():
    inicialitzar_db()
    estat_guardat = carregar_estat()

    termes_cerca = ['rupit', 'pruit', 'collsacabra', 'sallent de rupit', 'sant joan de fabregues']
    descartar_text = [
        'iuris', 'responsum', 'pro ', 'por el', 'manifiesto', 'allegatio', 
        'causa', 'pleito', 'notaria', 'notarial', 'arxiu notarial', 'liber',
        'escriptura', 'privilegi', 'sentencia', 'real provision', 'consell'
    ]

    total_trobades = 0

    for fons in ENDPOINTS:
        fons_nom = fons['nom']
        print(f"\n Connectant amb: {fons_nom}...")
        
        sickle = Sickle(fons['url'])
        token_actual = estat_guardat.get(fons_nom)

        try:
            if token_actual:
                print(f" 🔁 Reprenent la cerca des del punt guardat (Token: {token_actual[:20]}...)...")
                records = sickle.ListRecords(resumptionToken=token_actual)
            else:
                print(" 🟢 Iniciant cerca des del principi d'aquest fons...")
                records = sickle.ListRecords(metadataPrefix=fons['prefix'])

            revisats = 0

            while True:
                try:
                    record = next(records)
                    revisats += 1
                    
                    meta = getattr(record, 'metadata', {})
                    titol = meta.get('title', [''])[0] if meta.get('title') else ''
                    desc = meta.get('description', [''])[0] if meta.get('description') else ''
                    text_complet = f"{titol} {desc}".lower()

                    # Filtre 1: Fora textos legals o llibres
                    if any(paraula in text_complet for paraula in descartar_text):
                        continue

                    # Filtre 2: Paraules de cerca territorial
                    if any(terme in text_complet for terme in termes_cerca):
                        dates = meta.get('date', [''])
                        str_data = dates[0] if dates else 'Data no consta'
                        any_foto = extreure_any(str_data)

                        # Filtre 3: Anys exclusius de fotografia (1850 - 1960)
                        if any_foto and (any_foto < 1850 or any_foto > 1960):
                            continue

                        identifiers = meta.get('identifier', [])
                        url_orig, thumbnail = "", ""

                        for ident in identifiers:
                            if "http" in ident:
                                url_orig = ident
                                break

                        if "cdm/ref" in url_orig:
                            try:
                                parts = url_orig.split('/collection/')[1].split('/id/')
                                coll, img_id = parts[0], parts[1]
                                thumbnail = f"https://mdc.csuc.cat/digital/api/singleitem/image/{coll}/{img_id}/default.jpg"
                            except IndexError:
                                continue
                        elif "calaix.gencat.cat" in url_orig:
                            thumbnail = url_orig
                        else:
                            continue

                        identifier = record.header.identifier
                        creador = meta.get('creator', ['Autor desconegut'])[0] if meta.get('creator') else 'Autor desconegut'

                        guardar_fotografia((identifier, titol, creador, str_data, desc, url_orig, thumbnail))
                        total_trobades += 1

                        print(f"  📸 [{any_foto or 'S/D'}] {titol[:50]}...")

                    if revisats % 100 == 0:
                        # Anem desant la posició cada 100 registres analitzats
                        if hasattr(records, 'resumption_token') and records.resumption_token:
                            desar_estat(fons_nom, records.resumption_token.token)
                        print(f"    Analitzats {revisats} registres...")

                except StopIteration:
                    # Quan s'acaba un fons, esborrem el token guardat per a ell
                    desar_estat(fons_nom, None)
                    print(f" S'han analitzat tots els registres de {fons_nom}.")
                    break

        except KeyboardInterrupt:
            print("\n ⏸️ Cerca aturada per l'usuari. El punt de lectura s'ha guardat!")
            break
        except Exception as e:
            print(f" ⚠️ Aturat per avís del servidor: {e}")
            break

    print(f"\n Procés completat. S'han trobat i desat {total_trobades} fotografies primordials.")

if __name__ == '__main__':
    extreure_fotos_amb_pau()
