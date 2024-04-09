.PHONY: docker-build docker-run test

docker-build:
	docker build -t text-metrics-service . -f docker/dockerfile;

docker-run: docker-build
	docker run -it --rm -p 8505:8000 text-metrics-service;
	
test:
	cd core && python -m nose2
