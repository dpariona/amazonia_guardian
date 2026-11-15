import pytest
from app import app, db
from models import User, Detection

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Base de datos en memoria para pruebas
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_registro_y_login(client):
    # Probar registro
    response = client.post('/register', data={'username': 'admin_test', 'password': '123'}, follow_redirects=True)
    assert b'Registro exitoso' in response.data

    # Probar login
    response = client.post('/login', data={'username': 'admin_test', 'password': '123'}, follow_redirects=True)
    assert b'Logout' in response.data # Si ve el boton logout, esta logueado

def test_crud_deteccion(client):
    # 1. Loguearse como admin (el primer registro es admin)
    client.post('/register', data={'username': 'admin_test', 'password': '123'})
    client.post('/login', data={'username': 'admin_test', 'password': '123'})

    # 2. CREATE
    res = client.post('/api/detections', json={
        'latitude': -12.5, 'longitude': -70.0, 'sensor': 'MODIS', 'acq_date': '2026-10-01', 'confidence': 'high'
    })
    assert res.status_code == 201
    det_id = res.json['id']

    # 3. READ
    res = client.get('/api/detections')
    assert len(res.json) == 1
    assert res.json[0]['sensor'] == 'MODIS'

    # 4. UPDATE
    res = client.put(f'/api/detections/{det_id}', json={'sensor': 'VIIRS'})
    assert res.json['sensor'] == 'VIIRS'

    # 5. DELETE
    res = client.delete(f'/api/detections/{det_id}')
    assert res.status_code == 200

    # Verificar que la BD esté vacía
    res = client.get('/api/detections')
    assert len(res.json) == 0

def test_acceso_denegado_sin_login(client):
    # Intentar crear sin estar logueado debe dar error 401/403
    res = client.post('/api/detections', json={'latitude': 0, 'longitude': 0})
    assert res.status_code in [401, 403]