# app/api.py
from datetime import datetime
from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from .version import get_version
from .services import OpenSenseMapService
from .config import Config
   
# Prometheus metrics
REQUEST_COUNT = Counter('hivebox_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('hivebox_request_duration_seconds', 'Request duration')
TEMPERATURE_GAUGE = Counter('hivebox_temperature_readings_total', 'Temperature readings')

def create_app() -> Flask:
    """Create and configure Flask application"""
    app = Flask(__name__)

    # Initialize services
    osm_service = OpenSenseMapService()

    @app.before_request
    def before_request():
        """Record request metrics"""
        REQUEST_COUNT.labels(method=request.method, endpoint=request.endpoint).inc()

    @app.route('/version', methods=['GET'])
    def version():
        """Return the version of the deployed app"""
        return jsonify({
            "version": get_version(),
            "service": "HiveBox API"
        })

    @app.route('/temperature', methods=['GET'])
    def temperature():
        """Return current average temperature with status from senseBox data"""
        try:
            avg_temp, status = osm_service.get_average_temperature_with_status()

            if avg_temp is None:
                return jsonify({
                    "error": "Unable to fetch temperature data",
                    "temperature": None,
                    "status": "Unknown",
                    "timestamp": datetime.now().isoformat()
                }), 503

            # Record temperature reading
            TEMPERATURE_GAUGE.inc()

            return jsonify({
                "temperature": avg_temp,
                "status": status,
                "unit": "°C",
                "source": "openSenseMap",
                "sensebox_count": len(Config.get_sensebox_ids()),
                "thresholds": {
                    "cold": Config.get_temp_thresholds()[0],
                    "hot": Config.get_temp_thresholds()[1]
                },
                "timestamp": datetime.now().isoformat()
            })

        except Exception as e:
            return jsonify({
                "error": "Internal server error",
                "message": str(e)
            }), 500

    @app.route('/metrics', methods=['GET'])
    def metrics():
        """Return Prometheus metrics"""
        return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

    @app.route('/health', methods=['GET'])
    def health():
        """Health check endpoint"""
        return jsonify({
            "status": "healthy",
            "service": "HiveBox API",
            "version": get_version()
        })

    return app

# For development server
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)