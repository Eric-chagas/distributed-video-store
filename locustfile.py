from locust import HttpUser, task, between

class DistributedVideoStoreUser(HttpUser):
    wait_time = between(1, 3) 
    
    host = "http://localhost:8000" 

    @task(4) 
    def get_movie_details(self):
        self.client.get("/grpc/api/movies/1", name="/grpc/api/movies/[id]")

    @task(2)
    def consult_availability(self):
        self.client.get("/grpc/api/rent/consult/1", name="/grpc/api/rent/consult/[id]")