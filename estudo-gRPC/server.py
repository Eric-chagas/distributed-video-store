import grpc
from concurrent import futures
import movie_info_pb2
import movie_info_pb2_grpc

class MovieInfoServicer(movie_info_pb2_grpc.MovieInfoServicer):
    # Defining movie list to be searched and returned
    movies = [
        {
            "movie_id": 1,
            "movie_name": "Kids",
            "movie_release_year": 1995,
            "movie_genre": "Drama"
        },
        {
            "movie_id": 2,
            "movie_name": "Happiness",
            "movie_release_year": 1998,
            "movie_genre": "Comedy-Drama"
        },
        {
            "movie_id": 3,
            "movie_name": "Coherence",
            "movie_release_year": 2013,
            "movie_genre": "Sci-Fi / Thriller"
        },
        {
            "movie_id": 4,
            "movie_name": "The Untouchables",
            "movie_release_year": 1987,
            "movie_genre": "Crime / Drama"
        },
        {
            "movie_id": 5,
            "movie_name": "Mid90s",
            "movie_release_year": 2018,
            "movie_genre": "Coming-of-Age / Drama"
        },
        {
            "movie_id": 6,
            "movie_name": "Robot Dreams",
            "movie_release_year": 2023,
            "movie_genre": "Animation / Drama"
        },
        {
            "movie_id": 7,
            "movie_name": "Venus",
            "movie_release_year": 2006,
            "movie_genre": "Drama / Romance"
        },
        {
            "movie_id": 8,
            "movie_name": "The King of Staten Island",
            "movie_release_year": 2020,
            "movie_genre": "Comedy / Drama"
        },
        {
            "movie_id": 9,
            "movie_name": "Rocky",
            "movie_release_year": 1976,
            "movie_genre": "Drama / Sport"
        }
    ]

    
    # Implementing GetMovieInfo defined in proto file
    def GetMovieInfo(self, request, context):
        
        print(f"\nServer receiving \"Unary Call\" request for movie id: {request.movie_id}\n")
        
        # Get movie from list
        movie_response = next((movie for movie in self.movies if movie["movie_id"] == request.movie_id))
        
        return movie_info_pb2.MovieReply(
            movie_id=movie_response["movie_id"],
            movie_name=movie_response["movie_name"],
            movie_release_year=movie_response["movie_release_year"],
            movie_genre=movie_response["movie_genre"]
        )
    
    # Server Streaming method for returning movies to the client, one at a time
    def GetMoviesServerStream(self, request, context):
        
        print(f"\nServer receiving \"Server Streaming\" request for movie IDs: {request.movie_ids}\n")
        
        for movie_id in request.movie_ids:
            movie = next((m for m in self.movies if m["movie_id"] == movie_id), None)
            if movie:
                yield movie_info_pb2.MovieReply(**movie)
            else:
                print(f"Movie with ID {movie_id} not found")
                
    # Client streaming method for returning a list of movies at once, for several ids streamed by client
    def GetMoviesClientStream(self, request_iterator, context):
        
        print(f"\nServer receiving \"Client stream\" request...\n")

        movie_list = []
        for request in request_iterator:
            movie = next((m for m in self.movies if m["movie_id"] == request.movie_id), None)
            if movie:
                movie_list.append(movie_info_pb2.MovieReply(**movie))
        return movie_info_pb2.MovieListReply(movies=movie_list)

    # Bidirectional streaming method for returning one film at a time by each id streamed by client
    def GetMoviesBidirectionalStream(self, request_iterator, context):
        
        print(f"\nServer receiving \"Bidirectional stream\" request...\n")
        
        for request in request_iterator:
            movie = next((m for m in self.movies if m["movie_id"] == request.movie_id), None)
            if movie:
                yield movie_info_pb2.MovieReply(**movie)
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=8)) # Defining number of threads to process requests paralel
    movie_info_pb2_grpc.add_MovieInfoServicer_to_server(MovieInfoServicer(), server) 
    server.add_insecure_port('[::]:70001') # Defining server port as 70001
    server.start()
    print("gRPC server online and listening on port 70001...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
        
        