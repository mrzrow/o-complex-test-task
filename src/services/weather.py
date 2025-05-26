from abc import ABC, abstractmethod
from aiohttp import ClientSession

from src.api.weather import IWeatherApi


class IWeatherService(ABC):
    def __init__(self, weather_api: IWeatherApi):
        self.weather_api = weather_api

    @abstractmethod
    async def get_weather(self, city: str) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def suggest_cities(self, query: str, count: int = 5) -> list:
        raise NotImplementedError


class WeatherService(IWeatherService):
    def __init__(self, weather_api: IWeatherApi):
        super().__init__(weather_api)

    async def get_weather(self, city: str) -> dict:
        async with ClientSession() as session:
            geo_data = await self.weather_api.fetch_geo(
                session=session,
                name=city
            )
            if not geo_data:
                raise ValueError('City not found')

            location = geo_data[0]
            lat, lon = location['latitude'], location['longitude']

            weather_data = await self.weather_api.fetch_weather(
                session=session,
                latitude=lat,
                longitude=lon,
            )

            weather_code = weather_data.get('weathercode')
            weather_type = self.weather_api.weather_to_text(code=weather_code)
            return {
                'city': location['name'],
                'temperature': weather_data.get('temperature'),
                'weather': weather_type
            }

    async def suggest_cities(self, query: str, count: int = 5) -> list:
        async with ClientSession() as session:
            geo_data = await self.weather_api.fetch_geo(
                session=session,
                name=query,
                count=count
            )
            return list({item['name'] for item in geo_data})
