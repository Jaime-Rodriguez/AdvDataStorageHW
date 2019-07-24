import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime


from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start date<br/>"
        f"/api/v1.0/start date/end date"
    )


@app.route("/api/v1.0/precipitation")
def precipitaion():
    # Query precipitation by date
    session = Session(engine)
    prec_12mo = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-23').\
    filter(Measurement.prcp != 'NaN').order_by(Measurement.date).all()

    # Create a dictionary from the row data and append to a list of all_passengers
    prec = []
    for date, prcp in prec_12mo:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        prec.append(precip_dict)

    return jsonify(prec)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all the stations"""
    # Query all stations
    session = Session(engine)
    results = session.query(Station.name).all()

    # Convert list of tuples into normal list
    station_names = list(np.ravel(results))

    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def temps():
    """Return a list of all the temps by date"""
    # Query all stations
    session = Session(engine)
    tempResults = session.query(Measurement.date,Measurement.tobs).filter(Measurement.station=='USC00513117').filter(Measurement.date>'2016-08-23').all()

    # Convert list of tuples into normal list
    tempList = list(np.ravel(tempResults))

    return jsonify(tempList)


@app.route("/api/v1.0/<start_date>")
def calc_temps_start(start_date):
    start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    session = Session(engine)    
    temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_dt).all()
    temp_final = list(np.ravel(temps))
    return jsonify(temp_final) 
      

@app.route("/api/v1.0/<start_date>/<end_date>")
def calc_temps(start_date, end_date):
    start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_dt = datetime.strptime(end_date, "%Y-%m-%d").date()
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    session = Session(engine)    
    temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_dt).filter(Measurement.date <= end_dt).all()
    temp_final = list(np.ravel(temps))
    return jsonify(temp_final) 
     
if __name__ == '__main__':
    app.run(debug=True)
