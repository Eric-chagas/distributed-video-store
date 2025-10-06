#!/bin/bash

# Set virtualenv and set GO grpc plugins
source .venv/bin/activate
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
export PATH="$PATH:$(go env GOPATH)/bin"

# generate protobuffer files
python3 -m grpc_tools.protoc -I=protos --python_out=./rent-service/protobuff_gen --grpc_python_out=./rent-service/protobuff_gen ./protos/rent.proto
python3 -m grpc_tools.protoc -I=protos --python_out=./catalogue-service/protobuff_gen --grpc_python_out=./catalogue-service/protobuff_gen ./protos/catalogue.proto
protoc --go_out=./catalogue-service/protobuff_gen/ \
    --go-grpc_out=./catalogue-service/protobuff_gen/ \
    protos/catalogue.proto
