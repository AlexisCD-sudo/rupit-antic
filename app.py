from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)

# Plantilla de disseny per a la web (lleugera, neta i elegant)
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
            padding: 2.5rem 1rem; 
            border-bottom: 4px solid #8c6d58; 
        }
        header h1 { 
            margin: 0; 
            font-size: 2.5rem; 
            letter-spacing: 1px; 
            font-family: Georgia, serif; 
        }
        header p { 
            margin-top: 0.5rem; 
            opacity: 0.85; 
            font-style: italic; 
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
            transition: transform 0.2s; 
            border: 1px solid #e0ddd5; 
            display: flex; 
            flex-direction: column; 
        }
        .card:hover { 
            transform: translateY(-4px); 
            box-shadow: 0 8px 12px rgba(0,0,0,0.1); 
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
            line-height: 1.3;
        }
        .meta { 
            font-size: 0.85rem; 
            color: #666; 
            margin-bottom: 1rem; 
        }
        .meta span { 
            display: block; 
            margin-bottom: 0.2rem; 
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
        .btn:hover { 
            background: #6e5443; 
        }
        footer { 
            text-align: center; 
            padding: 2rem; 
            background: #e8e4d9; 
            margin-top: 3rem; 
            font-size: 0.85rem; 
            color: #555; 
            line-height: 1.5;
        }
        footer a { 
            color: #2c221e; 
            font-weight: bold; 
        }
    </style>
</head>
<body>

<header>
    <h1>Rupit Antic</h1>
    <p>Memòria fotogràfica i patrimoni històric de Rupit i el Collsacabra</p>
</header>

<div class="container">
    <div class="counter">
        S'han trobat <span>{{ fotos|length }}</span> fotografies històriques a l'arxiu
    </div>

    <div class="grid">
        {% for foto in fotos %}
        <div class="card">
            <img src="{{ foto[6] }}" alt="{{ foto[1] }}" loading="lazy" onerror="this.src='https://via.placeholder.com/300x200?text=Imatge+d%27Arxiu';">
            <div class="card-content">
                <div>
                    <h3>{{ foto[1] }}</h3>
                    <div class="meta">
                        <span><strong>Autor:</strong> {{ foto[2] }}</span>
                        <span><strong>Data:</strong> {{ foto[3] }}</span>
                    </div>
                </div>
                <a href="{{ foto[5] }}" target="_blank" class="btn">Veure fitxa a l'MDC</a>
            </div>
        </div>
        {% endfor %}
    </div>
</div>

<footer>
    <p><strong>Rupit Antic</strong> — Projecte digital sense ànim de lucre amb finalitat exclusivament cultural i divulgativa.</p>
    <p>Les fotografies mostrades procedeixen dels fons de la <a href="https://mdc.csuc.cat/" target="_blank">Memòria Digital de Catalunya</a>.</p>
</footer>

</body>
</html>
'''

@app.route('/')
def index():
    conn = sqlite3.connect('rupit_antic.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM fotografies ORDER BY data ASC')
    fotos = cursor.fetchall()
    conn.close()
    return render_template_string(HTML_TEMPLATE, fotos=fotos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
