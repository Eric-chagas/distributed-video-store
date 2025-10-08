package main

import (
	"context"
	"fmt"
	"log"
	"net"
	"google.golang.org/grpc"
	catalogueproto "distributed-video-store/catalogue-service/proto_generated"
)

// Define a struct Movie
type Movie struct {
	ID     int32
	Title  string
	Year   int32
	Genre  string
}

// gRPC server struct
type server struct {
	catalogueproto.UnimplementedCatalogueServiceServer
}

// Implementa o método GetMovie definido no .proto
func (s *server) GetMovie(ctx context.Context, req *catalogueproto.MovieRequest) (*catalogueproto.MovieResponse, error) {
	movies := []Movie{
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

	// Busca pelo ID requisitado
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

	// Caso não encontre, retorna um default
	return &catalogueproto.MovieResponse{
		Id:    req.Id,
		Title: "Not Found",
		Genre: "N/A",
		Year:  0,
	}, nil
}

func main() {
	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatalf("Failed to listen: %v", err)
	}

	s := grpc.NewServer()
	catalogueproto.RegisterCatalogueServiceServer(s, &server{})

	fmt.Println("Catalogue Service listening on port 50051...")
	if err := s.Serve(lis); err != nil {
		log.Fatalf("Failed to serve: %v", err)
	}
}
