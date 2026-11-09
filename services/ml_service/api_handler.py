"""Класс-обработчик запросов к API: загружает модель и выдаёт предсказание."""
import logging
import os
import pickle as pkl

import pandas as pd

logger = logging.getLogger('uvicorn.error')

# Внутри контейнера каталог с моделью подключается как /models,
# при локальном запуске из ml_service он лежит на уровень выше.
MODEL_PATHS = ('/models/model.pkl', '../models/model.pkl')

# Признаки в том порядке, в котором их ожидает модель.
# Список совпадает с research/production_columns.txt.
FEATURE_ORDER = [
    'Present_Price', 'Kms_Driven', 'Fuel_Type', 'Seller_Type',
    'Transmission', 'Owner', 'vehicle_type', 'car_age', 'kms_per_year',
]


class FastAPIHandler:
    """Загружает модель один раз при старте сервиса и отвечает на запросы."""

    def __init__(self, model_path: str | None = None):
        path = model_path or os.getenv('MODEL_PATH') or self._find_model()
        logger.info('Загрузка модели из %s', path)
        with open(path, 'rb') as f:
            self.model = pkl.load(f)
        logger.info('Модель загружена: %s', type(self.model).__name__)

    @staticmethod
    def _find_model() -> str:
        for candidate in MODEL_PATHS:
            if os.path.exists(candidate):
                return candidate
        raise FileNotFoundError(
            'Файл model.pkl не найден. Ожидался один из путей: '
            + ', '.join(MODEL_PATHS)
            + '. Получить модель: cd services/models && python get_model.py'
        )

    def predict(self, item_features: dict) -> float:
        """Предсказанная цена продажи в лакхах рупий."""
        item_df = pd.DataFrame([item_features])[FEATURE_ORDER]
        return float(self.model.predict(item_df)[0])
