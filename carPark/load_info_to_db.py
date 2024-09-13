import pandas as pd
from django.utils import timezone

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carPark_db.settings')
django.setup()

from carPark.models import CarParkInfo

def load_info(file):
    # some missing total carpark capacity info
    data = pd.read_excel(file)

    print(len(data))

    data['total_lots'] = data['total_lots'].fillna(0).astype(int)

    data['Location'] = data['Location'].fillna('0 0')

    data[['latitude', 'longitude']] = data['Location'].str.split(' ', expand=True)

    data['latitude'] = pd.to_numeric(data['latitude'], errors='coerce')
    data['longitude'] = pd.to_numeric(data['longitude'], errors='coerce')

    for index, row in data.iterrows():
        carpark_info = CarParkInfo(
            carpark_id=row['CarParkID'],
            name=row['Development'],
            lot_type=row['LotType'],
            total_capacity=row['total_lots'],
            agency=row['Agency'],
            latitude=row['latitude'],
            longitude=row['longitude'],
            last_updated = timezone.now(),
        )
        carpark_info.save()
    return {'status': 'successful'}

load_info('../carpark_complete_info.xlsx')
