# tests/test_integration.py
import pytest
import requests
import time
import json
from unittest.mock import patch
   
class TestIntegration:
    """Integration tests for HiveBox API"""
    
    @pytest.fixture(scope="class")
    def api_base_url(self):
        """Base URL for API testing"""
        return "http://localhost:5000"
    
    def test_version_endpoint_integration(self, api_base_url):
        """Test version endpoint returns correct structure"""
        response = requests.get(f"{api_base_url}/version")
        
        assert response.status_code == 200
        data = response.json()
        assert "version" in data
        assert "service" in data
        assert data["service"] == "HiveBox API"
    
    def test_health_endpoint_integration(self, api_base_url):
        """Test health endpoint returns healthy status"""
        response = requests.get(f"{api_base_url}/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_metrics_endpoint_integration(self, api_base_url):
        """Test metrics endpoint returns Prometheus format"""
        response = requests.get(f"{api_base_url}/metrics")
        
        assert response.status_code == 200
        assert "text/plain" in response.headers.get("content-type", "")
        assert "hivebox_requests_total" in response.text
    
    @patch('app.services.OpenSenseMapService.get_average_temperature_with_status')
    def test_temperature_endpoint_integration(self, mock_temp, api_base_url):
        """Test temperature endpoint with mocked data"""
        mock_temp.return_value = (23.5, "Good")
        
        response = requests.get(f"{api_base_url}/temperature")
        
        assert response.status_code == 200
        data = response.json()
        assert "temperature" in data
        assert "status" in data
        assert "thresholds" in data
        assert data["status"] in ["Too Cold", "Good", "Too Hot"]
    
    def test_api_error_handling(self, api_base_url):
        """Test API handles non-existent endpoints properly"""
        response = requests.get(f"{api_base_url}/nonexistent")
        assert response.status_code == 404
   
class TestOpenSenseMapIntegration:
    """Integration tests with real openSenseMap API"""
    
    def test_real_api_connectivity(self):
        """Test connectivity to real openSenseMap API"""
        # This test uses real API - mark as slow/integration
        url = "https://api.opensensemap.org/boxes/5eba5fbad46fb8001b799786"
        
        try:
            response = requests.get(url, timeout=10)
            assert response.status_code == 200
            data = response.json()
            assert "_id" in data
        except requests.RequestException:
            pytest.skip("openSenseMap API not accessible")