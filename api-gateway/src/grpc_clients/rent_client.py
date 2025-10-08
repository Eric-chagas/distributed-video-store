import grpc
from src.proto_generated import rent_pb2, rent_pb2_grpc

def check_availability(movie_id: int):
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = rent_pb2_grpc.RentServiceStub(channel)
        response = stub.CheckAvailability(rent_pb2.RentRequest(movie_id=movie_id))
        return {
            "available": response.available,
            "status": response.status
        }
