FROM python:3.11-slim

# Содержимое текущей директории (ml_service) копируется в /ml_service
COPY . /ml_service

# Каталог с моделью подключается снаружи при запуске контейнера
VOLUME /models

WORKDIR /ml_service

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Сборка образа (выполнять из каталога ml_service):
# docker build -t car-price-service:2 .

# Запуск контейнера:
# docker run -p 8000:8000 -v $(pwd)/../models:/models car-price-service:2
