import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from datetime import datetime
import datetime as dt

# 1. import Flask
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Station = Base.classes.station
Measurement = Base.classes.measurement

session = Session(engine)

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    return (
           f"List of previous years' temps: <a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
           f"List of all stations: <a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
           f"List of temps: <a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
           f"Stats of start date: <a href='/api/v1.0/start'>/api/v1.0/start</a><br/>"
           f"Stats of start and end date: <a href='/api/v1.0/start/end'>/api/v1.0/start/end</a><br/>"
           )


# 4. Define what to do when a user hits the /about route
@app.route("/api/v1.0/precipitation")
def precipitation():
    #Query dates
    dates = session.query(Measurement.date).filter(Measurement.date > "2017-04-30").all()
    #dateStrings = [datetime.strftime(x,'%Y-%m-%d') for x in dates]
    dateStrings = [str(x) for x in dates]
    temps = session.query(Measurement.tobs).filter(Measurement.date > "2017-04-30").all()
    dictDatesTemps = dict(zip(dateStrings, temps))
    #new_dict = {k: v for k, v in zip(dateStrings, temps)}
    #all_dates = list(np.ravel(new_dict))
    return jsonify(dictDatesTemps)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station).all()
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    temps = session.query(Measurement.tobs).filter(Measurement.date > "2017-04-30").all()
    return jsonify(temps)

@app.route("/api/v1.0/start")
def start():
    startTemp = input('Enter start temp date (YYYY-MM-DD) ')
    tempsQ = session.query(Measurement.tobs).filter(Measurement.date >= startTemp).all()
    tempInts = [float(str(x).replace("(","").replace(")","").replace(",","")) for x in tempsQ]
    minTemp = min(tempInts)
    maxTemp = max(tempInts)
    avgTemp = round(sum(tempInts)/len(tempsQ))
    tempsT = [minTemp, avgTemp, maxTemp]
    keys = ["TMIN","TAVG","TMAX"]
    dictTemps = dict(zip(keys, tempsT))
    return jsonify(dictTemps)

@app.route("/api/v1.0/start/end")
def end():
    startTemp = input('Enter start temp date (YYYY-MM-DD) ')
    endTemp = input('Enter end temp date (YYYY-MM-DD) ')
    tempsQ = session.query(Measurement.tobs).filter(Measurement.date > startTemp).filter(Measurement.date < endTemp).all()
    tempInts = [float(str(x).replace("(","").replace(")","").replace(",","")) for x in tempsQ]
    minTemp = min(tempInts)
    maxTemp = max(tempInts)
    avgTemp = round(sum(tempInts)/len(tempsQ))
    tempsT = [minTemp, avgTemp, maxTemp]
    keys = ["TMIN","TAVG","TMAX"]
    dictTemps = dict(zip(keys, tempsT))
    return jsonify(dictTemps)

if __name__ == "__main__":
    app.run(debug=True)
