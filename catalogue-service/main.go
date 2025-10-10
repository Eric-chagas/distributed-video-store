package main

import (
	"context"
	catalogueproto "distributed-video-store/catalogue-service/proto_generated"
	"fmt"
	"log"
	"net"

	"google.golang.org/grpc"
	"google.golang.org/protobuf/types/known/emptypb"
)

// Defining Movie response struct
type Movie struct {
	ID     int32
	Title  string
	Year   int32
	Genre  string
}

// Define catalogue server struct
type server struct {
	catalogueproto.UnimplementedCatalogueServiceServer
}

// Creating movie list "DB"
var	movies = []Movie{
	{1, "Kids", 1995, "Drama"},
	{2, "Happiness", 1998, "Comedy-Drama"},
	{3, "Coherence", 2013, "Sci-Fi / Thriller"},
	{4, "The Untouchables", 1987, "Crime / Drama"},
	{5, "Mid90s", 2018, "Coming-of-Age / Drama"},
	{6, "Robot Dreams", 2023, "Animation / Drama"},
	{7, "Venus", 2006, "Drama / Romance"},
	{8, "The King of Staten Island", 2020, "Comedy / Drama"},
	{9, "Rocky", 1976, "Drama / Sport"},
}

// Implements getMovie method defined in proto file
func (s *server) GetMovie(ctx context.Context, req *catalogueproto.MovieRequest) (*catalogueproto.MovieResponse, error) {
	// seraches for ID in movie "DB"
	for _, movie := range movies {
		if movie.ID == req.Id {
			return &catalogueproto.MovieResponse{
				Id:    movie.ID,
				Title: movie.Title,
				Genre: movie.Genre,
				Year:  movie.Year,
			}, nil
		}
	}

	// Return case not found
	return &catalogueproto.MovieResponse{
		Id:    req.Id,
		Title: "Not Found",
		Genre: "N/A",
		Year:  0,
	}, nil
}

// Implements grpc stress test method defined in proto file method STREAM
func (s *server) GRPCStressTestStream(in *emptypb.Empty, stream catalogueproto.CatalogueService_GRPCStressTestStreamServer) error {
	log.Println("Iniciando GRPCStressTest streaming...")

	for i := 1; i <= 100000; i++ {
		resp := &catalogueproto.MovieResponse{
			Id:    int32(i),
			Title: fmt.Sprintf("Movie %d", i),
			Genre: "Drama",
			Year:  2000 + int32(i%20),
		}

		if err := stream.Send(resp); err != nil {
			return fmt.Errorf("erro ao enviar resposta: %v", err)
		}

	}

	log.Println("Streaming finalizado com sucesso.")
	return nil
}

// Implements grpc stress test method defined in proto file method UNARY
func (s *server) GRPCStressTestUnary(ctx context.Context, in *emptypb.Empty) (*catalogueproto.MovieListResponse, error) {
	log.Println("Iniciando GRPCStressTest com lista única...")

	movies := make([]*catalogueproto.MovieResponse, 0, 100000)

	for i := 1; i <= 100000; i++ {
		movie := &catalogueproto.MovieResponse{
			Id:    int32(i),
			Title: fmt.Sprintf("Movie %d", i),
			Genre: "Drama",
			Year:  2000 + int32(i%20),
		}
		movies = append(movies, movie)
	}

	log.Printf("Gerados %d filmes.\n", len(movies))
	log.Println("Retornando lista completa...")

	return &catalogueproto.MovieListResponse{Movies: movies}, nil
}

// Run main
func main() {
	lis, err := net.Listen("tcp", ":50051")
	
	if err != nil {
		log.Fatalf("Failed to get Catalogue Server running on port 50051: %v", err)
	}

	s := grpc.NewServer(
		grpc.MaxRecvMsgSize(500*1024*1024),
    	grpc.MaxSendMsgSize(500*1024*1024),
	)
	
	catalogueproto.RegisterCatalogueServiceServer(s, &server{})

	fmt.Println("Catalogue Service listening on port 50051...")
	
	if err := s.Serve(lis); err != nil {
		log.Fatalf("Failed to serve: %v", err)
	}
}
