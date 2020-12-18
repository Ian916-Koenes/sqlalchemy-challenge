# imoot matplotlib and pandas toolkit
# Python SQL toolkit and Object Relational Mapper
# import flask
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

# create engine
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

# Create an app, being sure to pass __name__
app = Flask(__name__)

#create available routes 
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
# create precipitation route 
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all percipitarion values"""
    # Query all precipitations
    results = session.query(Measurement.date, Measurement.prcp).all()

    # close session 
    session.close()

    #create empty dictionary and run loop to place values in dict 
    all_precipitations = {}
    for date, prcp in results:
        all_precipitations[date] = prcp

    #return json for all precipitations 
    return jsonify(all_precipitations)

#create stations route 
@app.route("/api/v1.0/stations")
def stations():

    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #query all stations id's 
    stations = session.query(Station.station).all()
    
    # close session 
    session.close()

    # return json for all station id's 
    return jsonify(stations)

# create route for temps 
@app.route("/api/v1.0/tobs")
def tobs():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    #find previous year
    one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    #query temps 
    stations = session.query(Measurement.tobs)
    
    # filter for most active station, filter by date of previous year and jigher, and order by dates 
    main_stations = stations.filter(Measurement.station == 'USC00519281').filter(Measurement.date >= one_year).order_by(Measurement.date).all()

    #close session 
    session.close()

    # return json for temps of previous year 
    return jsonify(main_stations)

# create a starting route 
@app.route("/api/v1.0/<start>")
def calc_temps(start):
    
    # Create our session (link) from Python to the DB 
    session = Session(engine)

    # query min temp, max temp, avg temp and create start point 
    start_date=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    # close session
    session.close()

    #return json for start date 
    return jsonify(start_date)

# create a ending route 
@app.route("/api/v1.0/<start>/<end>")
def calc_temps2(start, end):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # query min temp, max temp, avg temp and create start point and end point
    end_date = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # close session 
    session.close()

    # return json for end date
    return jsonify(end_date)

# run app 
if __name__ == '__main__':
    app.run(debug=True)

