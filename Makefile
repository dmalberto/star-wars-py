
.PHONY: build up

build:
	docker build -t star-wars .

up:
	docker run -p 8000:8000 star-wars