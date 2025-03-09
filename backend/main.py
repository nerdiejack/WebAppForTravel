from fastapi import FastAPI
import os
from pymongo import MongoClient

app = FastAPI()

# Connect to MongoDB
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(mongo_uri)
db = client.travel_db

@app.get("/")
def read_root():
    return {"message": "Welcome to the Travel API!"}
