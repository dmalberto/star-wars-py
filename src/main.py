from src.planet import Planet
from fastapi import FastAPI

app = FastAPI()


@app.post("/planets")
async def add_planet(planet: Planet):
    return planet.insert()


@app.delete("/planets/{id}")
async def delete_planet(id: int):
    return Planet.delete(id)


@app.delete("/planets/all")
async def delete_all_planets():
    return Planet.delete_all()


@app.get("/planets")
async def get_planet(id: int = None, name: str = None):
    return Planet.get(id, name)
