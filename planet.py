from pydantic import BaseModel
from typing import Optional
import requests
import json
from mongo import Mongo

mongo = Mongo()
planets = mongo.get_collection()


class Planet(BaseModel):
    id: Optional[int]
    name: str
    climate: str
    terrain: str
    films_no: Optional[int]

    def get_films_no(self):
        content = requests.get(
            f"https://swapi.dev/api/planets/?search={self.name}").content
        results = json.loads(content)['results']
        return len(results[0]['films']) if len(results) > 0 else 0

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
        query = {}
        if id is not None:
            query.update({"_id": id})
        if name is not None:
            query.update({"name": name})
        return [planet for planet in planets.find(query)]

    @staticmethod
    def get_id():
        return len([planet for planet in planets.find({})]) + 1

    @staticmethod
    def delete(id):
        query = {"_id": id}
        planets.delete_one(query)
        return {"status": 200}
