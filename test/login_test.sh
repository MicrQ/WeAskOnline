#!/usr/bin/env bash
# Bash script to simulate a post request sent to the server

# return an error response
curl -X POST --location '127.0.0.1:5000/login' \
--form 'username="lawsonredeye"' \
--form 'password="I am groot"'

# logs a user based on the form input
curl -X POST --location '127.0.0.1:5000/login' \
--form 'username="lawsonredeye"' \
--form 'password="Iam groot"'