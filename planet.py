from pydantic import BaseModel
from typing import Optional
import requests
import json
from db import Db

db = Db()
planets = db.get_collection()


class Planet(BaseModel):
    id: Optional[int]
    name: str
    climate: str
    terrain: str
    films_no: Optional[int]

    def get_films_no(self):
        try:
            content = requests.get(
                f"https://swapi.dev/api/planets/?search={self.name}").content
            results = json.loads(content)['results']
            for r in results:
                return len(r['films']) if r['name'] == self.name else 0
        except:
            return 0

    def insert(self):
        planet = {
            '_id': self.id,
            'name': self.name,
            'climate': self.climate,
            'terrain': self.terrain,
            'films_no': self.films_no
        }
        try:
            planets.insert_one(planet)
            return {"status": 200, "response": planet}
        except:
            return {"status": 500, "message": "Internal server error"}

    @staticmethod
    def get(id, name):
        query = {}
        if id is not None:
            query.update({"_id": id})
        if name is not None:
            query.update({"name": name})
        try:
            response = [planet for planet in planets.find(query)]
            return {"status": 200, "response": response}
        except:
            return {"status": 500, "message": "Internal server error"}

    def get_id(self):
        try:
            atual_id = max(planet['_id'] for planet in planets.find({}))
        except:
            atual_id = 0
        return atual_id + 1

    @staticmethod
    def delete(id):
        query = {"_id": id}
        try:
            planets.delete_one(query)
            return {"status": 200, "message": "Delete success"}
        except:
            return {"status": 500, "message": "Internal server error"}

    @staticmethod
    def delete_all():
        try:
            planets.delete_many({})
            return {"status": 200, "message": "Delete success"}
        except:
            return {"status": 500, "message": "Internal server error"}
