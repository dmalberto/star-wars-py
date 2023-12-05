from pydantic import BaseModel
from typing import Optional
import requests
import json
from src.db import Db

db = Db()
planets = db.get_collection()


class Planet(BaseModel):
    id: Optional[int]
    name: str
    climate: str
    terrain: str
    films_no: Optional[int]

    def __get_films_no(self):
        try:
            content = requests.get(
                f"https://swapi.dev/api/planets/?search={self.name}").content
            results = json.loads(content)['results']
            for r in results:
                return len(r['films']) if r['name'] == self.name else 0
        except:
            return 0

    def __get_id(self):
        try:
            atual_id = max(planet['_id'] for planet in planets.find({}))
        except:
            atual_id = 0
        finally:
            return atual_id + 1

    def insert(self):
        self.id = self.__get_id()
        self.films_no = self.__get_films_no()
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
            return {"status": 500, "response": "Internal server error"}

    @staticmethod
    def get(id, name):
        query = {}
        if id is not None:
            query["_id"] = id
        if name is not None:
            query["name"] = name
        try:
            response = list(planets.find(query))
            return {"status": 200, "response": response}
        except:
            return {"status": 500, "response": "Internal server error"}

    @staticmethod
    def delete(id):
        query = {"_id": id}
        try:
            planets.delete_one(query)
            return {"status": 202, "response": "Delete success"}
        except:
            return {"status": 500, "response": "Internal server error"}

    @staticmethod
    def delete_all():
        try:
            planets.delete_many({})
            return {"status": 200, "response": "Delete success"}
        except:
            return {"status": 500, "response": "Internal server error"}
