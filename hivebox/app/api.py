# app/api.py
from datetime import datetime
from flask import Flask, jsonify
from .version import get_version
from .services import OpenSenseMapService
from .config import Config
   
def create_app() -> Flask:
    """Create and configure Flask application"""
    app = Flask(__name__)

    # Initialize services
    osm_service = OpenSenseMapService()

    @app.route("/", methods=["GET"])
    def root():
        """Root endpoint - simple status message"""
        return jsonify({
            "service": "HiveBox API",
            "status": "running",
            "available_endpoints": ["/version", "/temperature", "/health"]
        })

    @app.route('/version', methods=['GET'])
    def version():
        """Return the version of the deployed app"""
        return jsonify({
            "version": get_version(),
            "service": "HiveBox API"
        })

    @app.route('/temperature', methods=['GET'])
    def temperature():
        """Return current average temperature from senseBox data"""
        try:
            avg_temp = osm_service.get_average_temperature()

            if avg_temp is None:
                return jsonify({
                    "error": "Unable to fetch temperature data",
                    "temperature": None,
                    "timestamp": datetime.now().isoformat()
                }), 503

            return jsonify({
                "temperature": avg_temp,
                "unit": "°C",
                "source": "openSenseMap",
                "sensebox_count": len(Config.get_sensebox_ids()),
                "timestamp": datetime.now().isoformat()
            })

        except Exception as e:
            return jsonify({
                "error": "Internal server error",
                "message": str(e)
            }), 500

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