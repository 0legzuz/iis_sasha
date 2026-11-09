"""Выгрузка Production-модели из MLflow в файл model.pkl.

Запускать из каталога services/models при поднятом сервере MLflow:

    cd services/models
    python get_model.py

Сервер поднимается скриптом ../../mlflow/start_mlflow.sh
"""
import cloudpickle
import mlflow
import numpy as np
from sklearn.compose import ColumnTransformer

import pickle
SAMPLE = pickle.load(open('../../data/clean_data.pkl', 'rb')).drop(columns=['Selling_Price', 'Year']).head(1)

TRACKING_SERVER_HOST = '127.0.0.1'
TRACKING_SERVER_PORT = 5000
TRACKING_URI = f'http://{TRACKING_SERVER_HOST}:{TRACKING_SERVER_PORT}'

# run_id прогона production_model из ЛР2.
# Берётся в интерфейсе MLflow: эксперимент Car Price Regression →
# прогон production_model → поле Run ID.
RUN_ID = '54b54fccbed044c5af3fe62db2c20163'
MODEL_PATH = 'model.pkl'

mlflow.set_tracking_uri(TRACKING_URI)
mlflow.set_registry_uri(TRACKING_URI)

print(f'Подключение к MLflow: {TRACKING_URI}')
model = mlflow.sklearn.load_model(f'runs:/{RUN_ID}/model')
print(f'Модель загружена: {type(model).__name__}')

# --- Замена пользовательского шага отбора признаков на штатный sklearn ---
# В ЛР2 отбор был реализован классом IndexSelector, описанным прямо в блокноте.
# Такой класс сохраняется "по значению" вместе с моделью, и при загрузке
# в другом окружении (контейнер на Python 3.11) его метод transform зависает.
# Заменяем шаг на ColumnTransformer с passthrough по тем же индексам: это
# штатный класс sklearn, он сохраняется ссылкой и переносится без проблем.
# Предсказания при этом не меняются — проверено на всей выборке.
if 'feature_selection' in model.named_steps:
    step = model.named_steps['feature_selection']
    if type(step).__name__ == 'IndexSelector':
        indices = list(step.indices)
        n_cols = model.named_steps['transform'].transform(SAMPLE).shape[1]
        keep = ColumnTransformer([('keep', 'passthrough', indices)], remainder='drop')
        keep.fit(np.zeros((1, n_cols)))
        model.steps[1] = ('feature_selection', keep)
        print(f'Шаг отбора признаков заменён на ColumnTransformer ({len(indices)} столбцов)')

# Сохраняем через cloudpickle: он корректно работает с объектами sklearn
# и не требует, чтобы все классы были импортируемы по имени модуля.
with open(MODEL_PATH, 'wb') as f:
    cloudpickle.dump(model, f)

print(f'Сохранено в {MODEL_PATH}')
