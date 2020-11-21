from pydantic import BaseModel
from typing import Optional


class Planet(BaseModel):
    _id: Optional[int]
    name: str
    climate: str
    terrain: str
    films_no: Optional[str] = None

    def get_films_no(self):
        self.films_no = "Creu"
