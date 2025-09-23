# tests/test_services.py
import pytest
from unittest.mock import patch, MagicMock
import requests
from app.services import OpenSenseMapService
   
@pytest.fixture
def osm_service():
    """Create OpenSenseMapService instance"""
    return OpenSenseMapService()
   
@patch('app.services.requests.get')
def test_get_box_data_success(mock_get, osm_service):
    """Test successful box data retrieval"""
    mock_response = MagicMock()
    mock_response.json.return_value = {'_id': 'test_box', 'name': 'Test Box'}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    result = osm_service.get_box_data('test_box_id')
    
    assert result == {'_id': 'test_box', 'name': 'Test Box'}
    mock_get.assert_called_once()

@patch('app.services.requests.get')
def test_get_box_data_failure(mock_get, osm_service):
    """Test box data retrieval failure"""
    mock_get.side_effect = requests.exceptions.RequestException("Network error")
    
    result = osm_service.get_box_data('test_box_id')
    
    assert result is None

def test_get_sensebox_ids(osm_service):
    """Test senseBox ID configuration"""
    ids = osm_service.sensebox_ids
    assert isinstance(ids, list)
    assert len(ids) == 3
    assert '5eba5fbad46fb8001b799786' in ids