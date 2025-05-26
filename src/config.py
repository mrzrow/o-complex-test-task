import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel

env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)


class Settings(BaseModel):
    geo_url: str = os.environ.get('GEO_URL')
    weather_url: str = os.environ.get('WEATHER_URL')


settings = Settings()
