import grpc
import movie_info_pb2
import movie_info_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:70001') as channel:
        stub = movie_info_pb2_grpc.MovieInfoStub(channel) # using created channel to server
        request = movie_info_pb2.MovieListRequest(movie_ids=[1, 3, 5, 9])
        
        # Calling server streaming sending list of ids
        responses = stub.GetMoviesServerStream(request)
        
        for movie in responses:
            print("Movie ID: ", movie.movie_id)
            print("Movie name: ", movie.movie_name)
            print("Movie year: ", movie.movie_release_year)
            print("Movie genre: ", movie.movie_genre)
            print()

if __name__ == '__main__':
    run()