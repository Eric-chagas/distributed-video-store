from typing import Union
from fastapi import FastAPI
from src.grpc_clients.catalogue_client import get_movie
from src.grpc_clients.rent_client import check_availability
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Distributed Video Store API Gateway")

# CORS config
origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

