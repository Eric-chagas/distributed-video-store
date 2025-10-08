from typing import Union
from fastapi import FastAPI
from src.grpc_clients.catalogue_client import get_movie
from src.grpc_clients.rent_client import check_availability


app = FastAPI(title="Distributed Video Store API Gateway")

@app.get("/")
def read_root():
    return {"Status": "UP"}

# catalogue gRPC client call endpoint 
@app.get("/api/movies/{movie_id}")
def movie_details(movie_id: int):
    movie = get_movie(movie_id)
    return {**movie}

# rent gRPC client call endpoint
@app.get("/api/rent/consult/{movie_id}")
def consult(movie_id: int):
    rent = check_availability(movie_id=movie_id)
    return {**rent}

