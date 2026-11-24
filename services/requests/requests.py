import json
import os
import random
import time
from itertools import count
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def sample():
    bike = random.choice([False, False, True])
    age = random.randint(2, 17)
    kms = random.randint(1000, 120000)
    return {
        'Present_Price': round(random.uniform(0.4, 2.5) if bike else random.uniform(3, 32), 2),
        'Kms_Driven': kms, 'Fuel_Type': 'Petrol' if bike else random.choice(['Petrol', 'Diesel', 'CNG']),
        'Seller_Type': 'Individual' if bike else random.choice(['Individual', 'Dealer']),
        'Transmission': 'Manual' if bike else random.choice(['Manual', 'Automatic']),
        'Owner': random.randrange(3), 'vehicle_type': 'two_wheeler' if bike else 'car',
        'car_age': age, 'kms_per_year': round(kms / age),
    }


def main():
    base = os.getenv('API_URL', 'http://ml_service:8000').rstrip('/')
    for item_id in count(1):
        # Каждый десятый запрос проверяет валидацию тела и даёт HTTP 422.
        body = None if item_id % 10 == 0 else sample()
        request = Request(f'{base}/api/prediction?item_id={item_id}',
                          data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'})
        try:
            with urlopen(request, timeout=10) as response:
                print(response.status, response.read().decode(), flush=True)
        except HTTPError as error:
            print(error.code, error.read().decode(), flush=True)
        except (URLError, TimeoutError) as error:
            print(f'Сервис недоступен: {error}', flush=True)
        time.sleep(random.uniform(0, 5))


if __name__ == '__main__':
    main()
