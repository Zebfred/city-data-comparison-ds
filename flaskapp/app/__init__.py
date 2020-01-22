from flask import Flask, request, render_template, redirect, url_for
from decouple import config
from flask_pymongo import PyMongo
from flask_cors import CORS
from app.city_spelling_matcher import *
from app.charts import *
from app.data_rangle import *
from flask import json
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
import netaddr
from flask_sslify import SSLify

def create_app():
    app = Flask(__name__, static_url_path='/app/static')

    # Connect to MongoDB
    seattledata = seattle()
    data = data_loader()
    app.config["JSON_SORT_KEYS"] = False
    app.config['MONGO_URI'] = config('MONGO_URI')
    mongo = PyMongo(app)
    ACCESS_KEY = config('ACCESS_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = config('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    sslify = SSLify(app)
    CORS(app)

    class usip(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        from_ip = db.Column(db.BIGINT)
        to_ip = db.Column(db.BIGINT)
        country_code = db.Column(db.String(2))
        country = db.Column(db.String(35))
        state = db.Column(db.String(30))
        city = db.Column(db.String(30))


        def __init__(from_ip, to_ip, country_code, country, qty, state, city):
            self.id = id
            self.from_ip = from_ip
            self.to_ip = to_ip
            self.country_code = country_code
            self.country = country
            self.state = state
            self.city = city
    # Dynamic End Point
    @app.route(f"/")
    def home():
        return redirect(url_for('docs'))

    @app.route(f"/docs")
    def docs():
        plot = housingtest(seattledata)
        graphJSON = plot[0]
        ids = plot[1]
        content = plot[2]
        return render_template('start.html',
                               ids=ids,
                               graphJSON=graphJSON, content=content)


    @app.route(f"/{ACCESS_KEY}/citydata/<num>")
    def allcitydata(num):
      doc = mongo.db.alldata.find_one({'_id':int(num)})

      return jsonify(doc)

    @app.route(f"/{ACCESS_KEY}/matchcity/<words>")
    def spelling_matcher(words):
        data = data_loader()
        doc = check_spelling(data, words)
        return jsonify(doc)


    @app.route('/postjson', methods = ['POST'])
    def foo():
        data = request.get_json(force=True)
        return jsonify(data)

    @app.route(f'/{ACCESS_KEY}/ip_to_city/<ip>', methods=['GET'])
    def get_product(ip):
        try:
            dec_ip = convert_ip(ip)
            data_query = usip.query.filter((usip.from_ip <= int(dec_ip)) & (usip.to_ip >= int(dec_ip))).first()
            if data_query != None:
                city = data_query.city
                state = data_query.state
            else:
                city = 'Seattle'
                state = 'WA'
        except:
                city = 'Seattle'
                state = 'WA'
        city_id = force_id(data, f"{city} {state}")
        doc = mongo.db.alldata.find_one({'_id':int(city_id)})
        return jsonify(doc)

    @app.route(f'/{ACCESS_KEY}/ip_to_city2/<ip>', methods=['GET'])
    def get_product2(ip):
        try:
            data = data_loader()
            dec_ip = convert_ip(ip)
            data_query = usip.query.filter((usip.from_ip <= int(dec_ip)) & (usip.to_ip >= int(dec_ip))).first()
            if data_query != None:
                city = data_query.city
                state = data_query.state
            else:
                city = 'Seattle'
                state = 'WA'
        except:
                city = 'Seattle'
                state = 'WA'
        city_id = force_id(data, f"{city} {state}")
        doc = mongo.db.alldata.find_one({'_id':int(city_id)})
        return jsonify(doc)

    return app