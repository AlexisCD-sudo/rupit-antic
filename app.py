from flask import Flask, render_template_string, request
import sqlite3

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rupit Antic - Arxiu Fotogràfic</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
            background-color: #f4f1ea; 
            color: #333; 
            margin: 0; 
            padding: 0; 
        }
        header { 
            background-color: #2c221e; 
            color: #f4f1ea; 
            text-align: center; 
            padding: 2.5rem 1rem 1.5rem 1rem; 
            border-bottom: 4px solid #8c6d58; 
        }
        header h1 { 
            margin: 0; 
            font-size: 2.5rem; 
            font-family: Georgia, serif; 
        }
        header p { 
            margin-top: 0.5rem; 
            opacity: 0.85; 
            font-style: italic; 
        }
        
        /* Estils per al cercador */
        .search-container {
            margin-top: 1.5rem;
            display: flex;
            justify-content: center;
            gap: 0.5rem;
        }
        .search-container input[type="text"] {
            padding: 0.6rem 1rem;
            font-size: 1rem;
            border: 1px solid #8c6d58;
            border-radius: 4px;
            width: 70%;
            max-width: 450px;
        }
        .search-container button {
            padding: 0.6rem 1.2rem;
            background: #8c6d58;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 1rem;
            cursor: pointer;
            font-weight: bold;
        }
        .search-container button:hover {
            background: #6e5443;
        }
        .clear-btn {
            display: inline-block;
            margin-left: 0.5rem;
            color: #8c6d58;
            text-decoration: underline;
            font-size: 0.9rem;
        }

        .container { 
            max-width: 1200px; 
            margin: 2rem auto; 
            padding: 0 1rem; 
        }
        .counter {
            background: #e0ddd5;
            padding: 0.8rem;
            border-radius: 6px;
            margin-bottom: 1.5rem;
            font-weight: bold;
            color: #444;
            text-align: center;
        }
        .grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); 
            gap: 1.5rem; 
        }
        .card { 
            background: #fff; 
            border-radius: 8px; 
            overflow: hidden; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.05); 
            border: 1px solid #e0ddd5; 
            display: flex; 
            flex-direction: column; 
        }
        .card img { 
            width: 100%; 
            height: 220px; 
            object-fit: cover; 
            background: #e0e0e0; 
        }
        .card-content { 
            padding: 1rem; 
            flex-grow: 1; 
            display: flex; 
            flex-direction: column; 
            justify-content: space-between; 
        }
        .card h3 { 
            margin: 0 0 0.5rem 0; 
            font-size: 1.05rem; 
            font-family: Georgia, serif; 
            color: #1a1a1a; 
        }
        .meta { 
            font-size: 0.85rem; 
            color: #666; 
            margin-bottom: 1rem; 
        }
        .btn { 
            display: inline-block; 
            text-align: center; 
            background: #8c6d58; 
            color: white; 
            text-decoration: none; 
            padding: 0.5rem; 
            border-radius: 4px; 
            font-size: 0.85rem; 
            font-weight: bold; 
        }
        footer { 
            text-align: center; 
            padding: 2rem; 
            background: #e8e4d9; 
            margin-top: 3rem; 
            font-size: 0.85rem; 
            color: #555; 
        }
    </style>
</head>
<body>

<header>
    <h1>Rupit Antic</h1>
    <p>Memòria fotogràfica i patrimoni històric de Rupit i el Collsacabra</p>
    
    <!-- Formulari del Cercador -->
    <form class="search-container" method="GET" action="/">
        <input type="text" name="q" placeholder="Cerca per carrer, església, autor, any..." value="{{ query }}">
        <button type="submit">Cercar</button>
    </form>
</header>

<div class="container">
    <div class="counter">
        {% if query %}
            S'han trobat <span>{{ fotos|length }}</span> resultats per a «<strong>{{ query }}</strong>» 
            <a href="/" class="clear-btn">[Esborrar cerca]</a>
        {% else %}
            Mostrant <span>{{ fotos|length }}</span> fotografies històriques de l'arxiu
        {% endif %}
    </div>

    <div class="grid">
        {% for foto in fotos %}
        <div class="card">
            <img src="{{ foto[6] }}" alt="{{ foto[1] }}" loading="lazy">
            <div class="card-content">
                <div>
                    <h3>{{ foto[1] }}</h3>
                    <div class="meta">
                        <span><strong>Autor:</strong> {{ foto[2] }}</span><br>
                        <span><strong>Data:</strong> {{ foto[3] }}</span>
                    </div>
                </div>
                <a href="{{ foto[5] }}" target="_blank" class="btn">Veure fitxa a l'arxiu d'origen</a>
            </div>
        </div>
        {% endfor %}
    </div>
</div>

<footer>
    <p><strong>Rupit Antic</strong> — Arxiu digital i memòria fotogràfica de Rupit i Pruit.</p>
    <p style="margin-top: 0.5rem; opacity: 0.8; font-size: 0.8rem;">
        Aquest és un projecte personal sense ànim de lucre creat amb finalitats culturals, de preservació i divulgació del patrimoni històric local.
    </p>
</footer>
</body>
</html>
'''

@app.route('/')
def index():
    query = request.args.get('q', '').strip()
    conn = sqlite3.connect('rupit_antic.db')
    cursor = conn.cursor()
    
    if query:
        search_param = f"%{query}%"
        # Cerca la paraula clau al títol, la descripció, l'autor o la data
        cursor.execute('''
            SELECT * FROM fotografies 
            WHERE titol LIKE ? OR descripcio LIKE ? OR creador LIKE ? OR data LIKE ?
            ORDER BY data ASC
        ''', (search_param, search_param, search_param, search_param))
    else:
        cursor.execute('SELECT * FROM fotografies ORDER BY data ASC')
        
    fotos = cursor.fetchall()
    conn.close()
    return render_template_string(HTML_TEMPLATE, fotos=fotos, query=query)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
