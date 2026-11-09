#!/bin/sh
# Запуск локального MLflow-сервера.
# Выполнять из директории ./mlflow:  sh start_mlflow.sh
# Интерфейс после запуска: http://localhost:5000 или http://127.0.0.1:5000
#
# Хранилище экспериментов и реестр моделей — в СУБД sqlite (mlruns.db),
# артефакты моделей — в каталоге mlartifacts. Оба лежат рядом с этим скриптом.
#
# --allowed-hosts: MLflow 3 проверяет заголовок Host и по умолчанию отдаёт 403
# на часть локальных адресов. Перечисляем оба, чтобы интерфейс открывался
# и по localhost, и по 127.0.0.1.

ROOT=$(dirname "$PWD")

mlflow server \
    --host localhost \
    --port 5000 \
    --allowed-hosts "localhost:5000,127.0.0.1:5000,localhost,127.0.0.1" \
    --backend-store-uri "sqlite:///${ROOT}/mlflow/mlruns.db" \
    --registry-store-uri "sqlite:///${ROOT}/mlflow/mlruns.db" \
    --default-artifact-root "${ROOT}/mlflow/mlartifacts"
