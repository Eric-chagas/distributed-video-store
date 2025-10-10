import grpc
from google.protobuf.empty_pb2 import Empty
from src.proto_generated import catalogue_pb2, catalogue_pb2_grpc
import os


catalogue_host = os.getenv("CATALOGUE_SERVICE_HOST", "localhost")
catalogue_port = os.getenv("CATALOGUE_SERVICE_PORT", "50051")

def get_movie(movie_id: int):
    with grpc.insecure_channel(f'{catalogue_host}:{catalogue_port}') as channel:
        stub = catalogue_pb2_grpc.CatalogueServiceStub(channel)
        response = stub.GetMovie(catalogue_pb2.MovieRequest(id=movie_id))
        return {
            "id": response.id,
            "title": response.title,
            "genre": response.genre,
            "year": response.year
        }
        
# Calls grpc catalogue server for stress test with bigger response SERVER STREAM
def grpc_stress_test_stream():
    with grpc.insecure_channel(f'{catalogue_host}:{catalogue_port}') as channel:
        stub = catalogue_pb2_grpc.CatalogueServiceStub(channel)
        responses = stub.GRPCStressTestStream(Empty())
        movies = []
        for response in responses:
            movies.append({
                "id": response.id,
                "title": response.title,
                "genre": response.genre,
                "year": response.year
            })
        return movies

# Calls grpc catalogue server for stress test with bigger response UNARY CALL
def grpc_stress_test_unary():
    with grpc.insecure_channel(f"{catalogue_host}:{catalogue_port}") as channel:
        stub = catalogue_pb2_grpc.CatalogueServiceStub(channel)
        # Chama o método que agora retorna MovieList
        response = stub.GRPCStressTestUnary(Empty())
        
        # Acessa a lista de filmes
        movies = [
            {
                "id": movie.id,
                "title": movie.title,
                "genre": movie.genre,
                "year": movie.year
            }
            for movie in response.movies
        ]
        return movies
