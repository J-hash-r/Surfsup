# Import Flask
from flask import Flask, jsonify

# Dependencies and Setup
import numpy as np
import datetime as dt

# Python SQL Toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import StaticPool

# database connection/setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite",connect_args={"check_same_thread": False}, poolclass=StaticPool, echo=True)

Base = automap_base()
Base.prepare(engine, reflect=True) 

measurement = Base.classes.measurement
station = Base.classes.station

session = Session(engine)


app = Flask(__name__)


@app.route("/")

def welcome():
        return """<html>
        <h1>Hawaii Climate App (Flask API)</h1>
<img src="https://i.ytimg.com/vi/3ZiMvhIO-d4/maxresdefault.jpg" alt="Hawaii Weather"/>
<p>Precipitation Analysis:</p>
<ul>
  <li><a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a></li>
</ul>
<p>Station Analysis:</p>
<ul>
  <li><a href="/api/v1.0/stations">/api/v1.0/stations</a></li>
</ul>
<p>Temperature Analysis:</p>
<ul>
  <li><a href="/api/v1.0/tobs">/api/v1.0/tobs</a></li>
</ul>
<p>Start Day Analysis:</p>
<ul>
  <li><a href="/api/v1.0/2017-03-14">/api/v1.0/2017-03-14</a></li>
</ul>
<p>Start & End Day Analysis:</p>
<ul>
  <li><a href="/api/v1.0/2017-03-14/2017-03-28">/api/v1.0/2017-03-14/2017-03-28</a></li>
</ul>
</html> """

@app.route("/api/v1.0/precipitation")
def precipitation():
        
        one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
        prcp_data = session.query(m.date, m.prcp).\
                filter(m.date >= one_year_ago).\
                order_by(m.date).all()
        prcp_data_list = dict(prcp_data)
        return jsonify(prcp_data_list)

# Station Route
@app.route("/api/v1.0/stations")
def stations():
        stations_all = session.query(Station.station, Station.name).all()
        station_list = list(stations_all)
        return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
        one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
        tobs_data = session.query(measurement.date, m.tobs).\
                filter(m.date >= one_year_ago).\
                order_by(m.date).all()
        tobs_data_list = list(tobs_data)
        return jsonify(tobs_data_list)

@app.route("/api/v1.0/<start>")
def start_day(start):
        start_day = session.query(m.date, func.min(m.tobs), func.avg(m.tobs), func.max(m.tobs)).\
                filter(m.date >= start).\
                group_by(m.date).all()
        start_day_list = list(start_day)
        return jsonify(start_day_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end_day(start, end):
        start_end_day = session.query(m.date, func.min(m.tobs), func.avg(m.tobs), func.max(m.tobs)).\
                filter(m.date >= start).\
                filter(m.date <= end).\
                group_by(m.date).all()
        start_end_day_list = list(start_end_day)
        return jsonify(start_end_day_list)
