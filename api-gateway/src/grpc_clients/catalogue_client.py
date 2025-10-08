import grpc
from src.proto_generated import catalogue_pb2, catalogue_pb2_grpc


def get_movie(movie_id: int):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = catalogue_pb2_grpc.CatalogueServiceStub(channel)
        response = stub.GetMovie(catalogue_pb2.MovieRequest(id=movie_id))
        return {
            "id": response.id,
            "title": response.title,
            "genre": response.genre,
            "year": response.year
        }
