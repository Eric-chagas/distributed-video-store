import grpc
import movie_info_pb2
import movie_info_pb2_grpc
import time

def generate_movie_requests():
    for movie_id in [1, 4, 6, 9]:
        print(f"Client: Now sending movie_id {movie_id}")
        yield movie_info_pb2.MovieRequest(movie_id=movie_id)
        time.sleep(0.5) 

def run():
    with grpc.insecure_channel('localhost:70001') as channel:
        stub = movie_info_pb2_grpc.MovieInfoStub(channel) # using created channel to server        
        # Calling server streaming sending list of ids
        response = stub.GetMoviesClientStream(generate_movie_requests())
                
        for movie in response.movies:
            print("Movie ID: ", movie.movie_id)
            print("Movie name: ", movie.movie_name)
            print("Movie year: ", movie.movie_release_year)
            print("Movie genre: ", movie.movie_genre)
            print()

if __name__ == '__main__':
    run()