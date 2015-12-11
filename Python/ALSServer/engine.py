import os
import sys
import MySQLdb
from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating
import logging
logging.basicConfig(filename = 'engine.log',level=logging.DEBUG)
logger = logging.getLogger(__name__)

def getUsersFromDatabase():
    userDictionary={}
    mydb = MySQLdb.connect(host='localhost',
        user='pythonconnector',
        passwd='python1029',
        db='BeerRatings')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM users")
    queryResults = cursor.fetchall()
    cursor.close()
    mydb.close()
    for result in queryResults:
        userDictionary[result[1].decode('utf-8')]=result[0]
    return userDictionary

def parseDatafileLine(datafileLine):
    ##Parse a line of the data file using the specified regular expression pattern
    splitArray = datafileLine.split("\t")
    for x in range(0,len(splitArray)):
        splitArray[x]=splitArray[x].replace("\"",'')
    if splitArray[0]=='beer_id':
        return (splitArray,0)
    elif len(splitArray)<>23:
        ##this is a failed parse
        return (splitArray,-1)
    else:
        return (splitArray, 1)


class RecommendationEngine:
    ####A beer recommendation engine

    def _parseData(self, filename):
    #Parse a data file returns a RDD of parsed lines
        return (self.sc.textFile(filename, 4, True).map(parseDatafileLine))

    def _loadData(self,path):
    ##Load a data file, returns a RDD of parsed valid lines

        filename =  path
        raw = self._parseData(filename)
        failed = (raw
            .filter(lambda s: s[1] == -1)
            .map(lambda s: s[0]))
        valid = (raw
            .filter(lambda s: s[1] == 1)
            .map(lambda s: s[0])
            .cache())
        header = (raw
            .filter(lambda s: s[1]==0)
            .map(lambda s:s[0]))
        headerDict={}
        for line in header.take(1):
            for x in range(0,len(line)):
                headerDict[x]=line[x]
        return valid, headerDict

   
    def __count_and_average_ratings(self):
        ###Updates the beer ratings counts

        logger.info("Counting beer ratings...")
        self.beer_rating_counts_RDD = \
            self.ratings_RDD.map(lambda (a,b,c): (b, 1)).reduceByKey(lambda a,b:a+b)
        
    def __load_model(self):
        ####Load the ALS model

        logger.info("Loading the ALS model...")
        self.model = MatrixFactorizationModel.load(self.sc, os.path.join('models/ALSBeerFixed'))
        logger.info("ALS model loaded!")

    def __predict_ratings(self, user_and_beer_RDD):
        """Gets predictions for a given (user_id, beer_id) formatted RDD
        Returns: an RDD with format (beer_name, beer_rating)
        """
        predicted_RDD = self.model.predictAll(user_and_beer_RDD)
        predicted_rating_RDD = predicted_RDD.map(lambda x: (x.product, x.rating))
        predicted_rating_title_and_count_RDD = \
            predicted_rating_RDD.join(self.beer_id_name_RDD).join(self.beer_rating_counts_RDD)
        predicted_rating_title_and_count_RDD = \
            predicted_rating_title_and_count_RDD.map(lambda r: (r[1][0][1], r[1][0][0], r[1][1]))
        
        return predicted_rating_title_and_count_RDD

    def get_ratings_for_beer_ids(self, user_id, beer_ids):
        ###Given a user_id and a list of beer_ids, predict ratings for each beer

        requested_beers_RDD = self.sc.parallelize(beer_ids).map(lambda x: (user_id, x))
        # Get predicted ratings
        ratings = self.__predict_ratings(requested_beers_RDD).collect()

        return ratings

    def _removeUsers(self,inputRDD,minReviews):
        countPerUser = inputRDD.map(lambda (x,y):(x,1)).reduceByKey(lambda a,b:a+b)
        outRDD = inputRDD.join(countPerUser).filter(lambda (x,(y,z)):z>=minReviews)
        return outRDD.map(lambda (x,(y,z)):(x,y))
    
    def get_top_ratings(self, user_id, beers_count):
        ###Recommends up to beers_count beers to user_id
	min_ratings=5
        # Get pairs of (user_id, beer_id) for user_id unrated beers
        user_unrated_beers_RDD = self.ratings_RDD.filter(lambda rating: not rating[1]==user_id).map(lambda x: (user_id, x[0]))
        # Get predicted ratings
        ratings = self.__predict_ratings(user_unrated_beers_RDD).filter(lambda r: r[2]>=min_ratings).takeOrdered(movies_count, key=lambda x: -x[1])

        return ratings

    def __init__(self, sc, dataset_path):
        ####Init the recommendation engine given a Spark context and a dataset path

        logger.info("Starting up the Recommendation Engine: ")
        self.sc = sc
        self.__load_model()
        self.allBeer_Path = os.path.join(dataset_path,'AllBeer.txt')
        self.allBeer_RDD,self.headers = self._loadData(self.allBeer_Path)
        self.nonEmpty = self.allBeer_RDD.map(lambda x:(x[19],x)).filter(lambda (x,y):y[22]!='')
        self.beerByUser = self._removeUsers(self.nonEmpty,12)
        self.userDict = getUsersFromDatabase()
        self.ratings_RDD = self.allBeer_RDD.map(lambda (x,y):(userDict[x],y[0],y[13]))
        self.beer_id_name_RDD = self.allBeer_RDD.map(lambda (x,y):(y[0],y[1])).distinct()
        self.__count_and_average_ratings()
        self.__load_model
