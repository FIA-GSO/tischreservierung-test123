import pytest
from api import create_app
from freeTablesRequest import FreeTablesSchema 


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    
    return app.test_client()


def test_free_tables(app):
    route = "/FreeTables"
    
    payload = { "timestamp": "2022-02-02 17:25:00" }

    response = app.get(path = route, json = payload)

    length = len(response.json['bookings'])
    assert response.status_code == 200
    assert length == 1