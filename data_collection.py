from django.utils import timezone
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carPark_db.settings')
django.setup()

from carPark.models import CarParkAvailability, CarParkInfo

def scrape_data():
    driver_path = ChromeDriverManager().install()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1280,720")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    page_url = "https://justpark.capitaland.com/LotsAvail"
    driver.get(page_url)

    wait = WebDriverWait(driver, 10)

    try:
        wait.until(ec.presence_of_element_located((By.CLASS_NAME, "lots-form")))

        all_containers = driver.find_elements(By.CLASS_NAME, "lotsAvail-container")
        container = all_containers[4]

        listings = container.find_elements(By.CLASS_NAME, "listing-item")

        x = 67

        for listing in listings:
            try:
                mall_div = listing.find_element(By.CLASS_NAME, "mall")
                location_element = mall_div.find_element(By.CLASS_NAME, "heading")
                location_name = location_element.text
                count_element = mall_div.find_element(By.CLASS_NAME, "lotscount")
                availability = count_element.find_element(By.TAG_NAME, "span").text

                # lot_type C-> car Y-> MotorCycle
                # assume carpark is for car
                carpark_info, created = CarParkInfo.objects.get_or_create(
                    carpark_id=x,
                    lot_type="C",
                    defaults={
                        "name": location_name,
                        "agency": "CapitaLand",
                        "latitude":0,
                        "longitude": 0,
                        "total_capacity": 0,
                        "last_updated": timezone.now()
                    }
                )

                CarParkAvailability.objects.create(
                    info=carpark_info,
                    available_lot=int(availability),
                    last_updated=timezone.now()
                )

                x += 1
            except Exception as e:
                print(f"Error processing: {e}")
                continue
    finally:
        driver.quit()

    return {'status': 'successful'}

def pull_data():
    api_key = '9Zr4XojjSl+tiRQzEPlruw=='
    url = 'http://datamall2.mytransport.sg/ltaodataservice/CarParkAvailabilityv2'

    headers = {
        'AccountKey': api_key,
        'accept': 'application/json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['value'])
        df = df[['CarParkID', 'Development', 'Location', 'AvailableLots', 'LotType', 'Agency']]

        df[['latitude', 'longitude']] = df['Location'].str.split(' ', expand=True)

        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')

        df = df[df["LotType"] != "H"]

        for index, row in df.iterrows():
            try:
                carpark_info, created = CarParkInfo.objects.get_or_create(
                    carpark_id=row['CarParkID'],
                    lot_type=row['LotType'],
                    defaults={
                        "name": row['Development'],
                        "agency": row['Agency'],
                        "latitude": row['latitude'],
                        "longitude": row['longitude'],
                        "total_capacity": 0,
                        "last_updated": timezone.now()
                    }
                )

                CarParkAvailability.objects.create(
                    info=carpark_info,
                    available_lot=row['AvailableLots'],
                    last_updated=timezone.now()
                )

            except Exception as e:
                print(f"Error processing CarParkID {row['CarParkID']}: {e}")
                continue
    else:
        print(f"Error: {response.status_code}")

    return {'status': 'successful'}