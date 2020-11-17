import flask
import sys
import os

from pathlib import Path

app = flask.Flask(__name__)
app.config["DEBUG"] = True


images=[
    {
    'lat': 49.2699648,
    'lon': -123.1290368,
    'epoch': 1588704959.321,
    'orientation': -10.2
    }
]

sys.path.insert(0, os.getcwd()+"/SubDirectory")

image_metadata=images[0]

@app.route('/glare/api/v1.0/image_metadata', methods=['GET'])
def get_tasks():
    return isGlare(image_metadata)


@app.route('/', methods=['GET'])
def home():
    return "<h1>Glare Detection</p>"


from astropy.coordinates import get_sun, AltAz, EarthLocation
from astropy.time import Time
import datetime
from pysolar.solar import get_azimuth
import pytz


timezone = pytz.timezone("America/Los_Angeles")


def isGlare(image_metadata):
    # convert linux epoch in seconds to utc time
    utc_time = datetime.datetime.fromtimestamp(float(image_metadata['epoch']), tz=None)
    utc_time = timezone.localize(utc_time)
    sun_time = Time(utc_time)

    loca = EarthLocation.from_geodetic(image_metadata['lon'], image_metadata['lat']) 
    altaz = AltAz(obstime=sun_time, location=loca)


    azimuth_deg = get_azimuth(image_metadata['lat'], image_metadata['lon'], utc_time)

    zen_ang = get_sun(sun_time).transform_to(altaz).zen


    if(zen_ang<45 and azimuth_deg>30 ):
        return true;

    return false;

app.run()    