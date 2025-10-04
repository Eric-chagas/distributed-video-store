import grpc
import movie_info_pb2
import movie_info_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:70001') as channel:
        stub = movie_info_pb2_grpc.MovieInfoStub(channel) # using created channel to server
        response = stub.GetMovieInfo(movie_info_pb2.MovieRequest(movie_id=4)) # sending request for movie with id 4 and wating response
        print(response) # Printing single movie response

if __name__ == '__main__':
    run()