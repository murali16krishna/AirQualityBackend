from sqlalchemy import inspect

from app import db
from app.models import AirQuality
import pandas as pd
from sodapy import Socrata

class AirQualityService:

    @staticmethod
    def fetch_data():
        """
        This function queries the Socrata API for air quality data, processes it into a pandas DataFrame,
        and inserts the records into the database if they don't already exist.
        """
        client = Socrata("data.cityofnewyork.us", None)
        results = client.get("c3uy-2p5r", limit=18098)

        results_df = pd.DataFrame.from_records(results)
        results_df = results_df.dropna(
            subset=["unique_id", "indicator_id", "name", "measure_info", "geo_place_name", "time_period", "start_date",
                    "data_value"])

        for _, row in results_df.iterrows():
            existing = AirQuality.query.filter_by(unique_id=row["unique_id"]).first()

            if not existing:
                air_quality = AirQuality(
                    unique_id=row["unique_id"],
                    indicator_id=row["indicator_id"],
                    name=row["name"],
                    measure=row["measure_info"],
                    geo_place_name=row["geo_place_name"],
                    time_period=row["time_period"],
                    start_date=row["start_date"],
                    data_value=row["data_value"],
                )
                db.session.add(air_quality)

        db.session.commit()

    @staticmethod
    def get_paginated_data(filters, page, per_page):
        """Apply filters, paginate, and retrieve data."""
        query = AirQuality.query

        # query = AirQualityService.apply_filters(query, filters)
        query = AirQualityService.apply_dynamic_filters(query, filters)

        paginated_data = query.paginate(page=page, per_page=per_page, error_out=False)
        return paginated_data

    @staticmethod
    def get_distinct_geo_place_names():
        """Retrieve distinct geo_place_name values from the database."""
        distinct_geo_place_names = db.session.query(AirQuality.geo_place_name).distinct().order_by(
            AirQuality.geo_place_name).all()

        # distinct_geo_place_names is a list of tuples, so we extract the first element from each tuple
        geo_place_names = [name[0] for name in distinct_geo_place_names]
        return geo_place_names

    @staticmethod
    def apply_filters(query, filters):
        """Apply filters to the query based on the provided filters dictionary."""
        if "name" in filters and filters["name"]:
            query = query.filter(AirQuality.name.like(f"%{filters['name']}%"))

        if "geo_place_name" in filters and filters["geo_place_name"]:
            query = query.filter(AirQuality.geo_place_name.like(f"%{filters['geo_place_name']}%"))

        if "time_period" in filters and filters["time_period"]:
            query = query.filter(AirQuality.time_period.like(f"%{filters['time_period']}%"))

        return query

    @staticmethod
    def apply_dynamic_filters(query, filters):
        """Apply filters dynamically using model metadata."""
        model_columns = {column.key: column for column in inspect(AirQuality).columns}

        for key, value in filters.items():
            if key in model_columns and value:
                query = query.filter(model_columns[key].like(f"%{value}%"))

        return query
