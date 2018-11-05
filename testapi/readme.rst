TestApi
=========

Demo project showing django with django rest framework and imdb open api
consumption.

In order to setup project, please copy `docker-compose.local.yml.example`
without `.example` file extension and enter your own imdb api key.

To run project locally, please ensure that the newest version of docker and
docker-compose is installed and run `make server`. Application needs
`testapi` database for proper operation, database can be created on
`make bash` command by running `psql -U postgres -h postgres` and then
`CREATE DATABASE testapi;`.

Project tests can be run by writing `pytest` in docker container after
`make bash` command.
