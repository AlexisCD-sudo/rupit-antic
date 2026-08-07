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
            cursor: pointer;
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
        
        /* Botons d'acció */
        .actions {
            display: flex;
            gap: 0.5rem;
            margin-top: auto;
        }
        .btn { 
            flex: 1;
            display: inline-block; 
            text-align: center; 
            background: #8c6d58; 
            color: white; 
            text-decoration: none; 
            padding: 0.5rem 0.2rem; 
            border-radius: 4px; 
            font-size: 0.8rem; 
            font-weight: bold; 
            border: none;
            cursor: pointer;
        }
        .btn:hover {
            background: #6e5443;
        }
        .btn-outline {
            background: transparent;
            color: #8c6d58;
            border: 1px solid #8c6d58;
        }
        .btn-outline:hover {
            background: #e0ddd5;
            color: #2c221e;
        }

        /* Visor en Gran (Modal Lightbox) */
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.85);
            justify-content: center;
            align-items: center;
            flex-direction: column;
            padding: 1rem;
            box-sizing: border-box;
        }
        .modal img {
            max-width: 90%;
            max-height: 80vh;
            border-radius: 4px;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
        }
        .modal-caption {
            color: #fff;
            margin-top: 1rem;
            text-align: center;
            font-family: Georgia, serif;
            font-size: 1.1rem;
        }
        .close-modal {
            position: absolute;
            top: 20px;
            right: 35px;
            color: #fff;
            font-size: 40px;
            font-weight: bold;
            cursor: pointer;
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
            <img src="{{ foto[6] }}" alt="{{ foto[1] }}" loading="lazy" onclick="obrirGran('{{ foto[6] }}', '{{ foto[1]|replace("'", "\\'") }}')">
            <div class="card-content">
                <div>
                    <h3>{{ foto[1] }}</h3>
                    <div class="meta">
                        <span><strong>Autor:</strong> {{ foto[2] }}</span><br>
                        <span><strong>Data:</strong> {{ foto[3] }}</span>
                    </div>
                </div>
                
                <!-- Els dos botons d'acció -->
                <div class="actions">
                    <button class="btn btn-outline" onclick="obrirGran('{{ foto[6] }}', '{{ foto[1]|replace("'", "\\'") }}')">🔍 Ampliar</button>
                    <a href="{{ foto[5] }}" target="_blank" class="btn">🔗 Veure font</a>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>

<!-- Finestra Modal per veure la imatge en gran -->
<div id="imageModal" class="modal" onclick="tancarGran()">
    <span class="close-modal">&times;</span>
    <img id="modalImg" src="" alt="Imatge ampliada">
    <div id="modalCaption" class="modal-caption"></div>
</div>

<footer>
    <p><strong>Rupit Antic</strong> — Arxiu digital i memòria fotogràfica de Rupit i Pruit.</p>
    <p style="margin-top: 0.5rem; opacity: 0.8; font-size: 0.8rem;">
        Aquest és un projecte personal sense ànim de lucre creat amb finalitats culturals, de preservació i divulgació del patrimoni històric local.
    </p>
</footer>

<script>
    function obrirGran(url, titol) {
        var modal = document.getElementById("imageModal");
        var modalImg = document.getElementById("modalImg");
        var modalCaption = document.getElementById("modalCaption");
        
        modal.style.display = "flex";
        modalImg.src = url;
        modalCaption.innerText = titol;
    }

    function tancarGran() {
        document.getElementById("imageModal").style.display = "none";
    }

    // Tancar amb la tecla Escape
    document.addEventListener('keydown', function(event) {
        if (event.key === "Escape") {
            tancarGran();
        }
    });
</script>

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
        cursor.execute('''
            SELECT * FROM fotografies 
            WHERE (thumbnail LIKE 'http%') 
              AND (titol LIKE ? OR descripcio LIKE ? OR creador LIKE ? OR data LIKE ?)
            ORDER BY data ASC
        ''', (search_param, search_param, search_param, search_param))
    else:
        cursor.execute('''
            SELECT * FROM fotografies 
            WHERE thumbnail LIKE 'http%' 
            ORDER BY data ASC
        ''')
        
    fotos = cursor.fetchall()
    conn.close()
    return render_template_string(HTML_TEMPLATE, fotos=fotos, query=query)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
