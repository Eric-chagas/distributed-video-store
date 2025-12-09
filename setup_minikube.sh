#!/bin/bash

# Set virtualenv and set GO grpc plugins
source .venv/bin/activate
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
export PATH="$PATH:$(go env GOPATH)/bin"

# generate protobuffer files for python on api-gateway
python3 -m grpc_tools.protoc -I=./protos --python_out=./api-gateway/src/proto_generated --grpc_python_out=./api-gateway/src/proto_generated ./protos/rent.proto ./protos/catalogue.proto

# User protoletariat tool to fix protoc absolute imports for python
protol \
--create-package \
  --in-place \
  --python-out ./api-gateway/src/proto_generated \
  protoc --proto-path=./protos rent.proto catalogue.proto

# generate protobuffer files for Go lang on both services
protoc -I=./protos --go_out=paths=source_relative:./catalogue-service/proto_generated/ --go-grpc_out=paths=source_relative:./catalogue-service/proto_generated/ ./protos/catalogue.proto
protoc -I=./protos --go_out=paths=source_relative:./rent-service/proto_generated/ --go-grpc_out=paths=source_relative:./rent-service/proto_generated/ ./protos/rent.proto

# Build and run front-end and mapped port 5173
docker build -t video-store-frontend:latest ./frontend/
docker run -dit -p 5173:5173 --name video-store-frontend-container video-store-frontend:latest

# Start minikube cluster and switching to k8s context
minikube start

# Build docker images for backend
eval $(minikube docker-env)
docker build -t api-gateway:latest ./api-gateway
docker build -t catalogue-service:latest -f ./catalogue-service/Dockerfile-grpc ./catalogue-service
docker build -t catalogue-rest-service:latest -f ./catalogue-service/Dockerfile-rest ./catalogue-service
docker build -t rent-service:latest ./rent-service

# Apply k8s manifest files
kubectl apply -Rf manifest/

# Sleep 10 seconds to wait for running pods
sleep 10

# Port forward for front-end connection and run in new terminal
kubectl port-forward svc/api-gateway-service 8000:8000


