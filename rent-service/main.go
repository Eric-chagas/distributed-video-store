package main

import (
	"context"
	"fmt"
	"log"
	"net"
	"google.golang.org/grpc"
	rentproto "distributed-video-store/rent-service/proto_generated"
)

// Defining rent response response struct
type RentStatus struct {
	MovieId int32
	Available bool
	Status string
}

// Define rent server struct
type server struct {
	rentproto.UnimplementedRentServiceServer
}
// Creating rental status list for movies
var rent_status = []RentStatus{
	{1, true, "Disponível"},
	{2, false, "Alugado"},
	{3, false, "Alugado"},
	{4, true, "Disponível"},
	{5, false, "Alugado"},
	{6, true, "Disponível"},
	{7, false, "Alugado"},
	{8, true, "Disponível"},
	{9, true, "Disponível"},
}

// Implements CheckAvailability method defined in proto file
func (s* server) CheckAvailability(ctx context.Context, req *rentproto.RentRequest) (*rentproto.RentResponse, error) {
	// Searches for ID in rental status
	for _, status := range rent_status {
		if status.MovieId == req.MovieId {
			return &rentproto.RentResponse{
				MovieId: status.MovieId,
				Available: status.Available,
				Status: status.Status,

			}, nil
		}
	}

	// Return case not found
	return &rentproto.RentResponse{
		MovieId: req.MovieId,
		Available: false,
		Status: "Record not found",
	}, nil
}

// Run main
func main() {
	lis, err := net.Listen("tcp", ":50052")
	
	if err != nil {
		log.Fatalf("Failed to get Rent Server running on port 50052: %v", err)
	}

	s := grpc.NewServer()
	rentproto.RegisterRentServiceServer(s, &server{})

	fmt.Println("Rent Service online! Listening on port 50052...")

	if err := s.Serve(lis); err != nil {
		log.Fatalf("Failed to serve: %v", err)
	}
}
