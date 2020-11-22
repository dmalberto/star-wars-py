from planet import Planet
from fastapi import FastAPI

app = FastAPI()


@app.post("/planets")
def add_planet(planet: Planet):
    planet.id = planet.get_id()
    planet.films_no = planet.get_films_no()
    planet.insert()
    return {"status": 200, "response": planet}


@app.delete("/planets/{id}")
def delete_planet(id: str):
    return Planet.delete(id)


@app.get("/planets")
async def get_planet(id: int = None, name: str = None):
    response = Planet.get(id, name)
    return {"status": 200, "response": response}
