from flask import Blueprint
main = Blueprint('main', __name__)
 
import json
from engine import RecommendationEngine
 
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
from flask import Flask, request

import csv
import MySQLdb

@main.route("/userlist/<int:count>", methods=["GET"])
def getUserList(count):
    mydb = MySQLdb.connect(host='localhost',
        user='pythonconnector',
        passwd='python1029',
        db='BeerRatings')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM  users LIMIT %s", count)
    user_data = cursor.fetchall()
    cursor.close()
    mydb.close()
    return json.dumps(user_data)

@main.route("/beerlist/<int:count>", methods=["GET"])
def getBeerList(count):
    mydb = MySQLdb.connect(host='localhost',
        user='pythonconnector',
        passwd='python1029',
        db='BeerRatings')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM beers LIMIT %s", count)
    beer_data = cursor.fetchall()
    cursor.close()
    mydb.close()
    return json.dumps(beer_data)

@main.route("/topStyles/<int:user_id>", methods=["GET"])
def getTopStyles(user_id):
    mydb = MySQLdb.connect(host='localhost',
        user='pythonconnector',
        passwd='python1029',
        db='BeerRatings')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM topStyles WHERE user_id = %s", user_id)
    style_data = cursor.fetchall()
    cursor.close()
    mydb.close()
    return json.dumps(style_data)

@main.route("/topBrewers/<int:user_id>", methods=["GET"])
def getTopBrewers(user_id):
    mydb = MySQLdb.connect(host='localhost',
        user='pythonconnector',
        passwd='python1029',
        db='BeerRatings')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM topBrewers WHERE user_id = %s", user_id)
    brewer_data = cursor.fetchall()
    cursor.close()
    mydb.close()
    return json.dumps(brewer_data)

@main.route("/name/<int:user_id>",methods=["GET"])
def get_user_name(user_id):
    mydb = MySQLdb.connect(host='localhost',
        user='pythonconnector',
        passwd='python1029',
        db='BeerRatings')
    cursor = mydb.cursor()
    cursor.execute("SELECT user_name FROM users WHERE user_id = %s", user_id)
    user_data = cursor.fetchall()
    cursor.close()
    mydb.close()
    return json.dumps(user_data)

@main.route("/beer/<int:count>", methods=["GET"])
def getBeer(count):
    mydb = MySQLdb.connect(host='localhost',
        user='pythonconnector',
        passwd='python1029',
        db='BeerRatings')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM beers WHERE beer_id = %s", count)
    user_data = cursor.fetchall()
    cursor.close()
    mydb.close()
    return json.dumps(user_data)

@main.route("/<int:user_id>/ratings/top/<int:count>", methods=["GET"])
def top_ratings(user_id, count):
    logger.debug("User %s TOP ratings requested", user_id)
    top_ratings = recommendation_engine.get_top_ratings(user_id,count)
    return json.dumps(top_ratings)

@main.route("/<int:user_id>/ratings/<int:movie_id>", methods=["GET"])
def beer_ratings(user_id, movie_id):
    logger.debug("User %s rating requested for beer %s", user_id, movie_id)
    ratings = recommendation_engine.get_ratings_for_beer_ids(user_id, [beer_id])
    return json.dumps(ratings)

def create_app(spark_context, dataset_path):
    global recommendation_engine 
    recommendation_engine = RecommendationEngine(spark_context, dataset_path)    
    app = Flask(__name__)
    app.register_blueprint(main)
    return app 
