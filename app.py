from flask import Flask

app = Flask(__name__)

releves = [
    {"ville": "Paris", "temperature": 21},
    {"ville": "Lyon", "temperature": 26},
    {"ville": "Marseille", "temperature": 27},
]

@app.route('/sante')
def sante():
    return {"statut": "ok"}, 200

@app.route('/moyenne')
def moyenne_api():
    if not releves:
        return {"source": "memoire", "moyenne": 0.0}, 200
    moy = sum(r["temperature"] for r in releves) / len(releves)
    return {"source": "memoire", "moyenne": moy}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
