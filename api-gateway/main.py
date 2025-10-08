from typing import Union
from fastapi import FastAPI
from src.grpc_clients.catalogue_client import get_movie
from src.grpc_clients.rent_client import check_availability
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Distributed Video Store API Gateway")

# CORS config
# origins = [
#     "http://localhost",
#     "http://localhost:5173",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def read_root():
    return {"Status": "UP"}

# catalogue gRPC client call endpoint 
@app.get("/grpc/api/movies/{movie_id}")
def movie_details(movie_id: int):
    movie = get_movie(movie_id)
    return {**movie}

# rent gRPC client call endpoint
@app.get("/grpc/api/rent/consult/{movie_id}")
def consult(movie_id: int):
    rent = check_availability(movie_id=movie_id)
    return {**rent}

# catalogue rest client redirect endpoint 
@app.get("/rest/api/movies/{movie_id}")
def movie_details(movie_id: int):
    movie = get_movie(movie_id)
    return {**movie}

# rent rest client redirect endpoint
@app.get("/rest/api/rent/consult/{movie_id}")
def consult(movie_id: int):
    rent = check_availability(movie_id=movie_id)
    return {**rent}
