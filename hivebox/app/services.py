import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from .config import Config

class OpenSenseMapService:
       """Service to interact with openSenseMap API"""
       
       def __init__(self):
           self.api_base = Config.OPENSENSEMAP_API_BASE
           self.sensebox_ids = Config.get_sensebox_ids()
       
       def get_box_data(self, box_id: str) -> Optional[Dict]:
           """Get data for a specific senseBox"""
           try:
               url = f"{self.api_base}/boxes/{box_id}"
               response = requests.get(url, timeout=10)
               response.raise_for_status()
               return response.json()
           except requests.exceptions.RequestException as e:
               print(f"Error fetching box data for {box_id}: {e}")
               return None
       
       def get_temperature_data(self, box_id: str, hours: int = 1) -> List[Dict]:
           """Get temperature measurements for a box within specified hours"""
           try:
               box_data = self.get_box_data(box_id)
               if not box_data or 'sensors' not in box_data:
                   return []
               
               # Find temperature sensor
               temp_sensor = None
               for sensor in box_data['sensors']:
                   if sensor['title'].lower() in ['temperature', 'temperatur', 'temp']:
                       temp_sensor = sensor
                       break
               
               if not temp_sensor:
                   return []
               
               # Get measurements from last hour
               from_date = (datetime.now() - timedelta(hours=hours)).isoformat()
               url = f"{self.api_base}/boxes/{box_id}/sensors/{temp_sensor['_id']}/measurements"
               params = {'from-date': from_date}
               
               response = requests.get(url, params=params, timeout=10)
               response.raise_for_status()
               return response.json()
           
           except requests.exceptions.RequestException as e:
               print(f"Error fetching temperature data for {box_id}: {e}")
               return []
       
       def get_average_temperature_with_status(self) -> Tuple[Optional[float], str]:
           """Get average temperature with status classification"""
           avg_temp = self.get_average_temperature()
           
           if avg_temp is None:
               return None, "Unknown"
           
           cold_threshold, hot_threshold = Config.get_temp_thresholds()
           
           if avg_temp <= cold_threshold:
               status = "Too Cold"
           elif avg_temp >= hot_threshold:
               status = "Too Hot"
           else:
               status = "Good"
           
           return avg_temp, status
       
       def get_average_temperature(self) -> Optional[float]:
           """Get average temperature from all configured senseBoxes"""
           all_temps = []
           
           for box_id in self.sensebox_ids:
               measurements = self.get_temperature_data(box_id)
               for measurement in measurements:
                   try:
                       temp_value = float(measurement['value'])
                       # Basic validation: reasonable temperature range
                       if -50 <= temp_value <= 60:
                           all_temps.append(temp_value)
                   except (ValueError, KeyError):
                       continue
           
           if not all_temps:
               return None
           
           return round(sum(all_temps) / len(all_temps), 2)