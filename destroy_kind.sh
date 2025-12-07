#!/bin/bash

# Stop and remove frontend container
docker stop video-store-frontend-container
docker rm video-store-frontend-container

# Delete video-store pods
kubectl delete -Rf manifest/

helm uninstall monitoring

CLUSTER_NAME="video-store-kind-cluster"
echo "Removing kind cluster: ($CLUSTER_NAME)..."
kind delete cluster --name $CLUSTER_NAME
