# tests/test_api.py
import pytest
import json
from unittest.mock import patch, MagicMock
from app.api import create_app
   
@pytest.fixture
def client():
    """Create test client"""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
   
def test_version_endpoint(client):
    """Test /version endpoint returns correct response"""
    response = client.get('/version')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['version'] == '0.1.0'
    assert data['service'] == 'HiveBox API'

def test_health_endpoint(client):
    """Test /health endpoint returns healthy status"""
    response = client.get('/health')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'healthy'
    assert data['service'] == 'HiveBox API'
    assert data['version'] == '0.1.0'

@patch('app.services.OpenSenseMapService.get_average_temperature')
def test_temperature_endpoint_success(mock_get_temp, client):
    """Test /temperature endpoint with successful data"""
    mock_get_temp.return_value = 23.5
    
    response = client.get('/temperature')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['temperature'] == 23.5
    assert data['unit'] == '°C'
    assert data['source'] == 'openSenseMap'
    assert 'timestamp' in data

@patch('app.services.OpenSenseMapService.get_average_temperature')
def test_temperature_endpoint_no_data(mock_get_temp, client):
    """Test /temperature endpoint when no data available"""
    mock_get_temp.return_value = None
    
    response = client.get('/temperature')
    data = json.loads(response.data)
    
    assert response.status_code == 503
    assert data['temperature'] is None
    assert 'error' in data