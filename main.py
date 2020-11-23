from planet import Planet
from fastapi import FastAPI

app = FastAPI()


@app.post("/planets")
async def add_planet(planet: Planet):
    planet.id = planet.get_id()
    planet.films_no = planet.get_films_no()
    return planet.insert()


@app.delete("/planets/{id}")
async def delete_planet(id: int):
    return Planet.delete(id)


@app.get("/planets")
async def get_planet(id: int = None, name: str = None):
    return Planet.get(id, name)
