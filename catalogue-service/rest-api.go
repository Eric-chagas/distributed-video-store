package main

import (
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
)

// Defining Movie response struct
type Movie struct {
	ID     int32 	`json:"id"`
	Title  string	`json:"title"`
	Year   int32 	`json:"year"`
	Genre  string 	`json:"genre"`
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

// Get movies for stress test
func getMoviesRest(c* gin.Context) {
	c.IndentedJSON(http.StatusOK, movies)
}

func getMoviesRestStressTest(nResults int) []Movie {
	movies_stress_response := make([]Movie, 0, nResults) 
	for i := 0; i < nResults; i++ {
		m := Movie{
			ID: int32(i),
			Title: fmt.Sprintf("Movie %d", i),
			Year: int32(1960 + (i % 40)),
			Genre: []string{"Drama", "Comedy", "Action", "Sci-Fi"}[i%4],
		}
		movies_stress_response = append(movies_stress_response, m)
	}
	return movies_stress_response
}

func runStressTest(c* gin.Context){
	c.IndentedJSON(http.StatusOK, getMoviesRestStressTest(100000))
}

func main() {
	router := gin.Default()
	router.GET("rest/movies/", getMoviesRest)
	router.GET("rest/stress-test", runStressTest)
	router.Run("localhost:8080")
}