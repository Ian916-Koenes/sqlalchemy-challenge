from matplotlib import style
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement 
Station = Base.classes.station 

# Create our session (link) from Python to the DB
session = Session(engine) 

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all percipitarion values"""
    # Query all precipitations
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    all_precipitations = {}
    for date, prcp in results:
        all_precipitations[date] = prcp

    return jsonify(all_precipitations)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = session.query(Station.station).all()

    session.close()

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    stations = session.query(Measurement.tobs)
    
    main_stations = stations.filter(Measurement.station == 'USC00519281').filter(Measurement.date >= one_year).order_by(Measurement.date).all()

    session.close()

    return jsonify(main_stations)

@app.route("/api/v1.0/<start>")
def calc_temps(start):
    
    session = Session(engine)

    start_date=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    session.close()

    return jsonify(start_date)


@app.route("/api/v1.0/<start>/<end>")
def calc_temps2(start, end):

    session = Session(engine)

    end_date = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    return jsonify(end_date)


if __name__ == '__main__':
    app.run(debug=True)

