package main

import (
	"context"
	"fmt"
	"log"
	"net"
	"net/http"

	rentproto "distributed-video-store/rent-service/proto_generated"

	"google.golang.org/grpc"

	grpc_prometheus "github.com/grpc-ecosystem/go-grpc-prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
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

	go func() {
        log.Println("Rent service: Prometheus metrics server starting on port 9091...")
        http.Handle("/metrics", promhttp.Handler())
        // Prometheus scrape in port 9090
        if err := http.ListenAndServe(":9091", nil); err != nil { 
            log.Fatalf("Failed to run Prometheus metrics server: %v", err)
        }
    }()

	lis, err := net.Listen("tcp", ":50052")
	
	if err != nil {
		log.Fatalf("Failed to get Rent Server running on port 50052: %v", err)
	}

	s := grpc.NewServer(
		grpc.StreamInterceptor(grpc_prometheus.StreamServerInterceptor), 
        grpc.UnaryInterceptor(grpc_prometheus.UnaryServerInterceptor),
	)

	grpc_prometheus.Register(s)

	rentproto.RegisterRentServiceServer(s, &server{})

	fmt.Println("Rent Service online! Listening on port 50052...")

	if err := s.Serve(lis); err != nil {
		log.Fatalf("Failed to serve: %v", err)
	}
}
