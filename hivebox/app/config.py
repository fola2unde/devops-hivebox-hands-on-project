# app/config.py
import os
from typing import List
class Config:
    """Application configuration"""

    # Version
    VERSION = "0.2.0"  # Updated for Phase 4

    # openSenseMap API
    OPENSENSEMAP_API_BASE = "https://api.opensensemap.org"

    # Default senseBox IDs (can be overridden via environment)
    DEFAULT_SENSEBOX_IDS = [
        "5eba5fbad46fb8001b799786",
        "5c21ff8f919bf8001adf2488", 
        "5ade1acf223bd80019a1011c"
    ]

    # Temperature thresholds for status
    TEMP_COLD_THRESHOLD = 10
    TEMP_HOT_THRESHOLD = 37

    @classmethod
    def get_sensebox_ids(cls) -> List[str]:
        """Get senseBox IDs from environment or use defaults"""
        env_ids = os.getenv('SENSEBOX_IDS')
        if env_ids:
            return [id.strip() for id in env_ids.split(',')]
        return cls.DEFAULT_SENSEBOX_IDS

    @classmethod
    def get_temp_thresholds(cls):
        """Get temperature thresholds from environment or use defaults"""
        cold_threshold = float(os.getenv('TEMP_COLD_THRESHOLD', cls.TEMP_COLD_THRESHOLD))
        hot_threshold = float(os.getenv('TEMP_HOT_THRESHOLD', cls.TEMP_HOT_THRESHOLD))
        return cold_threshold, hot_threshold