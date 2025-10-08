FROM golang:1.25.1

WORKDIR /rent

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN go build -o server main.go

EXPOSE 50052

CMD ["./server"]
