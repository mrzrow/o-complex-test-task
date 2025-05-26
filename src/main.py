from fastapi import FastAPI, Request, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.services.weather import WeatherService
from src.depends.weather import get_weather_service


app = FastAPI()
app.mount('/static', StaticFiles(directory='static'))
templates = Jinja2Templates(directory='src/templates')



@app.get('/')
async def home(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.get('/weather')
async def get_weather(
    city: str = Query(..., min_length=1),
    service: WeatherService = Depends(get_weather_service)
):
    try:
        return await service.get_weather(city=city)
    except ValueError as e:
        return JSONResponse(status_code=404, content={'error': f'{e}'})
    except Exception as e:
        return JSONResponse(status_code=500, content={'error': f'Unknown error: {e}'})


@app.get('/suggest')
async def suggest_cities(
    query: str = Query(..., min_length=1),
    service: WeatherService = Depends(get_weather_service)
):
    try:
        return await service.suggest_cities(query=query)
    except Exception as e:
        return JSONResponse(status_code=500, content={'error': f'Unknown error: {e}'})
