import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

def test_sante_repond_ok():
    client = app.test_client()
    reponse = client.get("/sante")
    assert reponse.status_code == 200
    assert reponse.get_json()["statut"] == "ok"

def test_moyenne_sans_base():
    client = app.test_client()
    reponse = client.get("/moyenne")
    assert reponse.status_code == 200
    donnees = reponse.get_json()
    assert "moyenne" in donnees
