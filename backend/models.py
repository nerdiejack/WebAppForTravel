from pydantic import BaseModel

class City(BaseModel):
    name: str
    country: str
    population: int
    description: str

class Restaurant(BaseModel):
    name: str
    city: str
    address: str
    rating: float
