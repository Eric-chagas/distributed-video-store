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
