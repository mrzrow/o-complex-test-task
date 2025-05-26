from abc import ABC, abstractmethod
from aiohttp import ClientSession

from src.config import settings


class IWeatherApi(ABC):
    @staticmethod
    @abstractmethod
    async def fetch_geo(session: ClientSession, name: str, count: int = None) -> list:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def fetch_weather(session: ClientSession, latitude: int, longitude: int) -> dict:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def weather_to_text(code: int) -> str:
        raise NotImplementedError


class WeatherApi(IWeatherApi):
    def __init__(self):
        pass

    @staticmethod
    async def fetch_geo(session: ClientSession, name: str, count: int = None) -> list:
        url = settings.geo_url
        params = {'name': name}
        if count is not None:
            params['count'] = count

        async with session.get(
            url=url,
            params=params,
        ) as response:
            response_data: dict = await response.json()
            return response_data.get('results', [])

    @staticmethod
    async def fetch_weather(
        session: ClientSession,
        latitude: float,
        longitude: float
    ) -> dict:
        url = settings.weather_url
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'current_weather': 'true'
        }

        async with session.get(
            url=url,
            params=params
        ) as response:
            response_data: dict = await response.json()
            weather = response_data.get('current_weather', {})
            return weather

    @staticmethod
    def weather_to_text(code: int) -> str:
        mapping = {
            0: 'Clear sky', 1: 'Mainly clear',
            2: 'Partly cloudy', 3: 'Cloudy', 45: 'Fog', 48: 'Depositing rime fog', 51: 'Light drizzle', 53: 'Drizzle',
            55: 'Dense drizzle', 56: 'Light freezing drizzle', 57: 'Dense freezing drizzle', 61: 'Slight rain',
            63: 'Rain', 65: 'Heavy rain', 66: 'Light freezing rain', 67: 'Heavy freezing rain',
            71: 'Slight snow fall', 73: 'Snow fall', 75: 'Heavy snow fall', 77: 'Snow grains', 80: 'Rain showers',
            81: 'Heavy rain showers', 82: 'Violent rain showers', 85: 'Slight snow showers', 86: 'Heavy snow showers',
            95: 'Thunderstorm', 96: 'Thunderstorm with slight hail', 99: 'Thunderstorm with heavy hail'
        }
        return mapping.get(code, 'No information')
