from pymongo import MongoClient
import json


class Db():
    def __init__(self):
        self.credentials = self.__get_credentials()
        self.client = self.__connect()
        self.db = self.__get_database()

    def __get_credentials(self):
        with open('./src/config/credentials.json') as json_file:
            credentials = json.load(json_file)
        return credentials['mongodb']

    def __connect(self):
        login = f"{self.credentials['user']}:{self.credentials['pass']}"
        url = "star-wars-shard-00-00.eljo1.mongodb.net:27017,star-wars-shard-00-01.eljo1.mongodb.net:27017,star-wars-shard-00-02.eljo1.mongodb.net:27017"
        params = "ssl=true&replicaSet=atlas-tso1zz-shard-0&authSource=admin&retryWrites=true&w=majority"
        db = self.credentials['db']
        connection_string = f"mongodb://{login}@{url}/{db}?{params}"
        return MongoClient(connection_string)

    def __get_database(self):
        return self.client[self.credentials['db']]

    def get_collection(self):
        return self.db[self.credentials['collection']]
