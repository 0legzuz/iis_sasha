"""Микросервис предсказаний: цена подержанного транспорта.

Локальный запуск из каталога ml_service:

    uvicorn main:app --reload

Документация и форма для тестовых запросов: http://localhost:8000/docs
"""
from typing import Literal

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field

from api_handler import FastAPIHandler

app = FastAPI(
    title='Car Price Prediction Service',
    description='Сервис предсказаний модели из ЛР2 (RandomForestRegressor). '
                'Цены в лакхах индийских рупий, 1 лакх = 100 000 ₹.',
    version='1.0',
)
app.handler = FastAPIHandler()


class VehicleFeatures(BaseModel):
    """Признаки объявления. Значения по умолчанию подставляются в форму /docs."""

    Present_Price: float = Field(5.59, description='Цена нового экземпляра, лакхов')
    Kms_Driven: int = Field(27000, description='Пробег, км')
    Fuel_Type: Literal['Petrol', 'Diesel', 'CNG'] = Field('Petrol', description='Тип топлива')
    Seller_Type: Literal['Dealer', 'Individual'] = Field('Dealer', description='Тип продавца')
    Transmission: Literal['Manual', 'Automatic'] = Field('Manual', description='Коробка передач')
    Owner: int = Field(0, description='Число предыдущих владельцев')
    vehicle_type: Literal['car', 'two_wheeler'] = Field('car', description='Тип транспорта')
    car_age: int = Field(6, description='Возраст, лет')
    kms_per_year: int = Field(4500, description='Пробег в год, км')


@app.get('/')
def root():
    return {'Hello': 'World'}


@app.post('/api/prediction')
def make_prediction(item_id: int, item_features: VehicleFeatures):
    """Предсказание цены продажи для одного объявления."""
    price = app.handler.predict(item_features.model_dump())
    return {
        'item_id': item_id,
        'predict': round(price, 4),
    }


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
