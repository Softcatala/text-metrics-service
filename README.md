# Introduction

A proof of concept of a Catalan style checker that complements LanguageTool

# Docker container

Use ```docker/build-docker.sh``` to build the Docker container

Use ```docker/run-docker.sh``` to execute the Docker container

Use locally:

* ```http://localhost:8505/metrics?text=hola``` to get metrics only
* ```http://localhost:8505/check?text=hola``` to get metrics and rules
