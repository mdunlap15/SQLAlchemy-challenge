import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start_date><br/>"
        f"/api/v1.0/<start_date>/<end_date><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    first_date = session.query(Measurement.date).order_by(Measurement.date).first()
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    date_prcp = session.query(Measurement.date, func.max(Measurement.prcp)).group_by(Measurement.date).\
    filter(Measurement.date > year_ago)

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_dates = []
    for date, prcp in date_prcp:
        dict = {}
        dict["date"] = date
        dict["prcp"] = prcp
        all_dates.append(dict)

    return jsonify(all_dates)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    all_stations = []
    for id, station, name, latitude, longitude, elevation in stations:
        dict = {}
        dict["id"] = id
        dict["station"] = station
        dict["name"] = name
        dict["latitude"] = latitude
        dict["longitude"] = longitude
        dict["elevation"] = elevation
        all_stations.append(dict)
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    year_ago = dt.date(2017, 8, 18) - dt.timedelta(days=365)
    most_active = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date > year_ago).all()
    most_active_tobs = []
    for date, tobs in most_active:
        dict = {}
        dict['date'] = date
        dict['tobs'] = tobs
        most_active_tobs.append(dict)
    return jsonify(most_active_tobs)

@app.route("/api/v1.0/<start_date>")
def calc_temps_start(start_date):
    tobs_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    tobs_stats_all = []
    for min, avg, max in tobs_stats:
        dict = {}
        dict['min'] = min
        dict['avg'] = avg
        dict['max'] = max
        tobs_stats_all.append(dict)
    return jsonify(tobs_stats_all)


@app.route("/api/v1.0/<start_date>/<end_date>")
def calc_temps_start_end(start_date, end_date):
    tobs_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    tobs_stats_all = []
    for min, avg, max in tobs_stats:
        dict = {}
        dict['min'] = min
        dict['avg'] = avg
        dict['max'] = max
        tobs_stats_all.append(dict)
    return jsonify(tobs_stats_all)






if __name__ == '__main__':
    app.run(debug=True)
