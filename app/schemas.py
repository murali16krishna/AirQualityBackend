from app import ma
from app.models import AirQuality

class AirQualitySchema(ma.SQLAlchemySchema):
    class Meta:
        model = AirQuality

    id = ma.auto_field()
    unique_id = ma.auto_field()
    indicator_id = ma.auto_field()
    name = ma.auto_field()
    measure = ma.auto_field()
    geo_place_name = ma.auto_field()
    time_period = ma.auto_field()
    start_date = ma.auto_field()
    data_value = ma.auto_field()
