from typing import Optional
from planet import Planet
from fastapi import FastAPI
from pymongo import MongoClient
import json

app = FastAPI()

client = MongoClient('127.0.0.1', 27017)
db = client['star-wars-py']
planets = db['planets']


@app.post("/planets")
def add_planet(planet: Planet):
    planet.get_films_no()
    return planet


@app.delete("/planets/{id}")
def delete_planet(id: str, q: Optional[str] = None):
    return {"status": 200}


@app.get("/planets")
async def get_planet(id: int = None, name: str = None):
    if name is not None:
        response = planets.find_one({"name": name})
    elif id is not None:
        response = planets.find_one({"_id": id})
    else:
        response = planets.find_one()
    return json.loads(json.dumps(response))
