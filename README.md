# O-Complex Test Task

This is a simple web application that allows users to check the current weather in any city.
By entering the name of a city, the app displays the current temperature and general weather conditions (e.g. clear, cloudy, etc.).

## Run

Rename `.env-template` to `.env`

### Manually:

1. Instal dependencies from `requirements.txt`
2. Run `uvicorn src.main:app`

### Docker:

1. Run `docker build -t [image_name] .`
2. Run `docker run -p [port:port] [image_name]`

## Examples

![Start Page](docs/result.jpg)

![Search](docs/search.jpg)

![Result](docs/result.jpg)
