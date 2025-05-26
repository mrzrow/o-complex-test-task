from fastapi import Depends

from src.services.weather import WeatherService
from src.api.weather import IWeatherApi, WeatherApi


def _get_weather_api():
    return WeatherApi


def get_weather_service(weather_api: IWeatherApi = Depends(_get_weather_api)):
    return WeatherService(weather_api=weather_api)
