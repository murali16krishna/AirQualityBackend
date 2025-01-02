from flask import request, jsonify, Blueprint
from app.services import AirQualityService
from app.schemas import AirQualitySchema

api_bp = Blueprint("api", __name__)
air_quality_schema = AirQualitySchema(many=True)

@api_bp.route("/", methods=["GET"])
def home():
    """Home route for the API."""
    return "Welcome to the Air Quality API!", 200

@api_bp.route("/air-quality", methods=["GET"])
def get_air_quality():
    """Fetch paginated air quality data with optional filters.

    Optional Query Parameters:
    - page: Page number (default: 1).
    - per_page: Number of items per page (default: 10).
    - name: Filter by the indicator name.
    - geo_place_name: Filter by geographic location.
    - time_period: Filter by the time period.
    """
    try:
        page = request.args.get("page", "1")
        per_page = request.args.get("per_page", "10")
        page = int(page) if page.isdigit() else 1
        per_page = int(per_page) if per_page.isdigit() else 10

        filters = request.args.to_dict()
        filters.pop("page", None)
        filters.pop("per_page", None)

        # Fetch paginated data with applied filters
        paginated_data = AirQualityService.get_paginated_data(filters, page, per_page)

        return jsonify({
            "data": air_quality_schema.dump(paginated_data.items),
            "total": paginated_data.total,
            "pages": paginated_data.pages,
            "current_page": paginated_data.page,
            "per_page": paginated_data.per_page,
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route("/air-quality/distinct-geo-place-names", methods=["GET"])
def get_distinct_geo_place_names():
    """Get a list of distinct geographic place names."""
    try:
        geo_place_names = AirQualityService.get_distinct_geo_place_names()
        return jsonify({"distinct_geo_place_names": geo_place_names}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route("/air-quality/fetch", methods=["POST"])
def fetch_air_quality():
    """Fetch air quality data from the external API and save to the database."""
    try:
        AirQualityService.fetch_data()
        return jsonify({"message": "Data fetched successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
