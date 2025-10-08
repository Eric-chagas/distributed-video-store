import grpc
from src.proto_generated import rent_pb2, rent_pb2_grpc
import os


rent_host = os.getenv("RENT_SERVICE_HOST", "localhost")
rent_port = os.getenv("RENT_SERVICE_PORT", "50052")

def check_availability(movie_id: int):
    with grpc.insecure_channel(f'{rent_host}:{rent_port}') as channel:
        stub = rent_pb2_grpc.RentServiceStub(channel)
        response = stub.CheckAvailability(rent_pb2.RentRequest(movieId=movie_id))
        return {
            "available": response.available,
            "status": response.status
        }
