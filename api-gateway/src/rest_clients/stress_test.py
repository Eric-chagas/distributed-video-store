import requests


def rest_stress_test():
    api_base_url = "http://localhost:8080"
    movies = requests.get(f"{api_base_url}/rest/stress-test")
    return movies.json()
