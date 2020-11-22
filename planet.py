from pydantic import BaseModel
from typing import Optional
import requests
import json
from pymongo import MongoClient

with open('./config/credentials.json') as json_file:
    credentials = json.load(json_file)
client = MongoClient(
    f"mongodb://{credentials['mongodb']['user']}:{credentials['mongodb']['pass']}@star-wars-shard-00-00.eljo1.mongodb.net:27017,star-wars-shard-00-01.eljo1.mongodb.net:27017,star-wars-shard-00-02.eljo1.mongodb.net:27017/{credentials['mongodb']['db']}?ssl=true&replicaSet=atlas-tso1zz-shard-0&authSource=admin&retryWrites=true&w=majority"
)
db = client['star-wars-py']
planets = db['planets']


class Planet(BaseModel):
    id: Optional[int]
    name: str
    climate: str
    terrain: str
    films_no: Optional[int]

    def get_films_no(self):
        results = json.loads(
            requests.get(f"https://swapi.dev/api/planets/?search={self.name}").
            content)['results']
        if len(results) > 0:
            return len(results[0]['films'])
        else:
            return 0

    def insert(self):
        planet = {
            '_id': self.id,
            'name': self.name,
            'climate': self.climate,
            'terrain': self.terrain,
            'films_no': self.films_no
        }
        planets.insert_one(planet)

    @staticmethod
    def get(id, name):
        if id is not None:
            p = {"_id": id}
        elif name is not None:
            p = {"name": name}
        else:
            p = {}
        return [r for r in planets.find(p)]

    @staticmethod
    def get_id():
        return len([r for r in planets.find({})]) + 1

    @staticmethod
    def delete(id):
        planets.delete_one({"_id": id})
        return {"status": 200}
