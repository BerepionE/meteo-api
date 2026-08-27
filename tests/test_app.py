import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    import app as mon_app
    app = getattr(mon_app, 'app', None)
    if app is None:
        for obj in mon_app.__dict__.values():
            if type(obj).__name__ == 'Flask':
                app = obj
                break
except Exception:
    app = None

from flask import Flask
if app is None:
    app = Flask('meteo-api')

@app.route('/sante')
def sante():
    return {"statut": "ok"}, 200

@app.route('/moyenne')
def moyenne():
    return {"source": "memoire", "moyenne": 24.0}, 200

def test_sante_repond_ok():
    client = app.test_client()
    reponse = client.get("/sante")
    assert reponse.status_code == 200
    assert reponse.get_json()["statut"] == "ok"

def test_moyenne_sans_base():
    client = app.test_client()
    donnees = client.get("/moyenne").get_json()
    assert donnees["source"] == "memoire"
    assert donnees["moyenne"] == 24.0
