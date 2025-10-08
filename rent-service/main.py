import grpc
from concurrent import futures
import time

from proto_generated import rent_pb2, rent_pb2_grpc

class RentService(rent_pb2_grpc.RentServiceServicer):
    def CheckAvailability(self, request, context):
        return rent_pb2.RentResponse(
            movie_id=request.movie_id,
            available=True,
            status="Disponível"
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rent_pb2_grpc.add_RentServiceServicer_to_server(RentService(), server)
    server.add_insecure_port('[::]:50052')
    print("Rent Service rodando na porta 50052...")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
