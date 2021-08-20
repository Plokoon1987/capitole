from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

def get_data(data, parent, get_list):
    '''Gets desired data from Weather API Json response'''
    dictio = {}
    for item in get_list:
        dictio[item] = data[parent][item]
    return dictio


class ModelExpandMixin:
    '''Provides Models with additional functionality'''

    @classmethod
    def get_or_create(cls, data, default=None):
        '''Gets an object with the parameters provided in the data dicionary
        If it can't get find an object it will create one

        The defaults parameter is used to populate the rest of the data in the object
        '''

        obj = cls.query.filter_by(**data).first()
        if obj:
            if default:
                for key, value in default.items():
                    setattr(obj, key, value)
        else:
            if default:
                data = dict(data, **default)
            obj = cls(**data)
            db.session.add(obj)

        db.session.commit()
        return obj

    def get_dict(self, columns=None):
        '''Returns a dictionary with fields from an object
        If no columns are specified all fields are returned
        '''
        if not columns:
            columns = [column.name for column in self.__table__.columns]

        return {column: getattr(self, column) for column in columns}


class Locality(db.Model, ModelExpandMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    country = db.Column(db.String(100))
    days = db.relationship('Day', backref='locality')
    hours = db.relationship('Hour', backref='locality')


class Day(db.Model, ModelExpandMixin):
    id = db.Column(db.Integer, primary_key=True)
    locality_id = db.Column(db.Integer,
                            db.ForeignKey('locality.id'),
                            nullable=False)
    name = db.Column(db.String(100))
    date = db.Column(db.String(100))
    temperature_max = db.Column(db.Integer)
    temperature_min = db.Column(db.Integer)
    icon = db.Column(db.String(100))
    text = db.Column(db.String(100))
    humidity = db.Column(db.Integer)
    wind = db.Column(db.Integer)
    wind_direction = db.Column(db.String(100))
    icon_wind = db.Column(db.String(100))
    sunrise = db.Column(db.String(100))
    sunset = db.Column(db.String(100))
    moonrise = db.Column(db.String(100))
    moonset = db.Column(db.String(100))
    moon_phases_icon = db.Column(db.String(100))


class Hour(db.Model, ModelExpandMixin):
    id = db.Column(db.Integer, primary_key=True)
    locality_id = db.Column(db.Integer,
                            db.ForeignKey('locality.id'),
                            nullable=False)
    name = db.Column(db.String(100))
    date = db.Column(db.String(100))
    temperature = db.Column(db.Integer)
    text = db.Column(db.String(100))
    humidity = db.Column(db.Integer)
    pressure = db.Column(db.Integer)
    icon = db.Column(db.String(100))
    wind = db.Column(db.Integer)
    wind_direction = db.Column(db.String(100))
    icon_wind = db.Column(db.String(100))


@app.route('/')
def index():
    return jsonify({'msg': "It's working!"})


@app.route('/update_data')
def update_data():
    '''Populates data in the database. It updates data everytime it is called'''

    # Fetching Data
    url = 'https://api.tutiempo.net/json/?lan=es&apid=zwDX4azaz4X4Xqs&lid=3768'
    req = requests.get(url)

    # Preparing data to insert
    data = req.json()


    # Location
    loc_list = ['name', 'country']
    loc_data = get_data(data, 'locality', loc_list)
    loc = Locality.get_or_create(loc_data)


    # Days
    day_list = ['date', 'temperature_max', 'temperature_min', 'icon', 'text',
                'humidity', 'wind', 'wind_direction', 'icon_wind', 'sunrise',
                'sunset', 'moonrise', 'moonset', 'moon_phases_icon']
    day_parents = ['day{}'.format(day) for day in range(1, 8)]

    for parent in day_parents:
        day_data = {'locality': loc,
                    'name': parent}
        default = get_data(data, parent, day_list)
        day = Day.get_or_create(day_data, default=default)


    # Hours
    h_list = ['date', 'temperature', 'text', 'humidity', 'pressure', 'icon',
              'wind', 'wind_direction', 'icon_wind']
    h_parents = ['hour{}'.format(day) for day in range(1, 26)]

    for parent in h_parents:
        h_data = {'locality': loc,
                  'name': parent}
        default = get_data(data['hour_hour'], parent, h_list)
        hour = Hour.get_or_create(h_data, default=default)


    dictio = {'msg': 'Los datos se han actualizado correctamente'}
    return jsonify(dictio)


@app.route('/data/day/<string:day>')
def get_day(day):
    '''Returns the specific object as a json response'''
    obj = Day.query.filter_by(name=day).first()
    if obj:
        return jsonify(obj.get_dict())
    else:
        return jsonify({'msg': 'El elemento está fuera del rango esperado'}), 404


@app.route('/data/hour/<string:hour>')
def get_hour(hour):
    '''Returns the specific object as a json response'''
    obj = Hour.query.filter_by(name=hour).first()
    if obj:
        return jsonify(obj.get_dict())
    else:
        return jsonify({'msg': 'El elemento está fuera del rango esperado'}), 404


db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
