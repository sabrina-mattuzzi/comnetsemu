#!/bin/bash

docker build -t dinamic_router:latest --file ./Dockerfile . && docker image prune -f