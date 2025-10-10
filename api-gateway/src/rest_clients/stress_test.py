import requests
import os


def rest_stress_test():
    catalogue_host = os.getenv("CATALOGUE_REST_SERVICE_HOST", "localhost")
    catalogue_port = os.getenv("CATALOGUE_REST_SERVICE_PORT", "8080")

    api_base_url = f"http://{catalogue_host}:{catalogue_port}"
    movies = requests.get(f"{api_base_url}/rest/stress-test")
    return movies.json()
