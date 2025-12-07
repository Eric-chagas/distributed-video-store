#!/bin/bash

# Stop and remove frontend container
docker stop video-store-frontend-container
docker rm video-store-frontend-container

# Delete video-store pods
kubectl delete -Rf manifest/

# Take minikube down
minikube delete
