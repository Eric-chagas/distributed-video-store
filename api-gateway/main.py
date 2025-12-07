from typing import Union
from fastapi import FastAPI
from src.grpc_clients.catalogue_client import get_movie, grpc_stress_test_stream, grpc_stress_test_unary
from src.grpc_clients.rent_client import check_availability
from src.rest_clients.stress_test import rest_stress_test
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Summary, Counter
from prometheus_fastapi_instrumentator import Instrumentator
from contextlib import asynccontextmanager

GRPC_CALL_LATENCY = Summary(
    'grpc_client_call_duration_seconds', 
    'Tempo de resposta das chamadas GRPC de cliente para Catalogue/Rent', 
    ['service', 'method'] # Labels para categorizar a chamada (qual serviço/método)
)

@asynccontextmanager
async def lifespan_event_handler(app: FastAPI):
    
    print("Prometheus metrics exposed in /metrics")
    yield
    print("api shutting down")

app = FastAPI(title="Distributed Video Store API Gateway", lifespan=lifespan_event_handler)

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

Instrumentator().instrument(app).expose(
    app, 
    endpoint="/metrics", 
)
print("Prometheus metrics middleware added and exposed in /metrics")


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

# Comparision of gRPC and Rest endpoints

# catalogue rest client redirect endpoint for stress test
@app.get("/rest/stresstest")
def getAllMoviesRest():
    movies = rest_stress_test()
    return {"rest_stress_test_result": movies}

# catalogue gRPC client redirect call for stress test SERVER STREAM
@app.get("/grpc/stresstest/stream")
def getAllMoviesGrpcStream():
    movies = grpc_stress_test_stream()
    return {"grpc_stress_test_result": movies}

# catalogue gRPC client redirect call for stress test UNARY
@app.get("/grpc/stresstest/unary")
def getAllMoviesGrpcUnary():
    movies = grpc_stress_test_unary()
    return {"grpc_stress_test_result": movies}