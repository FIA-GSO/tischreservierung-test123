import pytest
from api import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    
    #yield app.test_client()
    return app.test_client()


def test_hello_world(app):
    route = "/"
    response = app.get(route)
    assert response.status_code == 200
    assert b"<h1>Hello, World!</h1>" in response.data          # Erläuterungen bis hier sind in \testFlaskSimple


def test_hello_person_arguments(app):
    route = "/person"
    payload = {                                                 # Dictionary ist für beide Tests identisch
        "vorname": "Bud",
        "nachname": "Spencer"
    }
    
    response = app.post(path = route, query_string = payload)   # query_string setzt die Inhalte eines Dicts hinter das ? in der URL

    assert response.status_code == 200
    assert b"Hello, Bud Spencer" in response.data


def test_hello_person_json(app):
    route = "/person/json"
    payload = {
        "vorname": "Bud",
        "nachname": "Spencer"
    }
    
    response = app.post(path = route, json=payload)             # json wandelt ein Dict in ein json um

    assert response.status_code == 200
    assert b"Hello, Bud Spencer" in response.data