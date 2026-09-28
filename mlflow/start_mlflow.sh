#!/bin/sh
# Запуск локального MLflow-сервера.
# Выполнять из директории ./mlflow:  sh start_mlflow.sh
# Интерфейс после запуска: http://localhost:5000
#
# Хранилище экспериментов и реестр моделей — в СУБД sqlite (mlruns.db),
# артефакты моделей — в каталоге mlartifacts. Оба лежат рядом с этим скриптом.

ROOT=$(dirname "$PWD")

mlflow server \
    --host localhost \
    --port 5000 \
    --backend-store-uri "sqlite:///${ROOT}/mlflow/mlruns.db" \
    --registry-store-uri "sqlite:///${ROOT}/mlflow/mlruns.db" \
    --default-artifact-root "${ROOT}/mlflow/mlartifacts"
