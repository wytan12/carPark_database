from contextlib import asynccontextmanager
from threading import Thread

from asgiref.sync import sync_to_async
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import os
import django
import time

from data_collection import scrape_data, pull_data

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carPark_db.settings')
django.setup()

from carPark.models import CarParkAvailability, CarParkInfo


def run_tasks():
    while True:
        if int(time.time()) % 1800 == 0:
            scrape_data()
            pull_data()
            time.sleep(5)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """ background task starts at startup """
    Thread(target=run_tasks, daemon=True).start()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.get('/')
def root():
    return {"message": "Hello!"}


@app.get("/carpark_info")
def get_carpark_info():
    carpark_info = list(CarParkInfo.objects.all())
    carpark_info_list = []
    for info in carpark_info:
        info_data = {
            'id': info.id,
            'carpark_id': info.carpark_id,
            'name': info.name,
            'lot_type': info.lot_type,
            'latitude': info.latitude,
            'longitude': info.longitude,
            'total_capacity': info.total_capacity,
            'agency': info.agency,
            'last_updated': info.last_updated,
        }
        carpark_info_list.append(info_data)

    return carpark_info_list


@app.get("/carpark_availability")
def get_carparks():
    carparks = list(CarParkAvailability.objects.all())
    carpark_availability = []
    for c in carparks:
        carpark_data = {
            'id': c.id,
            'info_id': c.info_id,
            'available_lot': c.available_lot,
            'last_updated': c.last_updated,
        }
        carpark_availability.append(carpark_data)

    return carpark_availability

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
