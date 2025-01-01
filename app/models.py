from app import db

class AirQuality(db.Model):
    __tablename__ = "air_quality"

    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(255), nullable=False, unique=True)
    indicator_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    measure = db.Column(db.String(255), nullable=False)
    geo_place_name = db.Column(db.String(255), nullable=False)
    time_period = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.String(255), nullable=False)
    data_value = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<AirQuality {self.unique_id}>"
