# Описание проекта

Проект решает задачу **регрессии**: по характеристикам объявления о продаже подержанного
транспорта (год выпуска, цена нового экземпляра, пробег, тип топлива, коробка передач,
число владельцев) предсказать запрашиваемую цену `Selling_Price`.

Исходная выборка: [Car Price Prediction (used cars)](https://www.kaggle.com/datasets/vijayaadithyanvg/car-price-predictionused-cars/data)
— 301 объявление, 8 признаков. Все цены указаны в лакхах индийских рупий (1 лакх = 100 000 ₹).

# Запуск

Для запуска проекта под ОС GNU/Linux необходимо выполнить команды:

```shell
git clone <адрес репозитория>
cd car-price-prediction
python3 -m venv .venv_car_price
source .venv_car_price/bin/activate
python3 -m pip install -r requirements.txt
```

Активация виртуального окружения:

```shell
source .venv_car_price/bin/activate
```

Деактивация:

```shell
deactivate
```

Запуск Jupyter для работы с блокнотом:

```shell
jupyter notebook eda/eda.ipynb
```

### Данные

Файлы с данными в репозиторий не коммитятся. Перед запуском блокнота нужно скачать
датасет и положить его в директорию `./data/` под именем `car_data.csv`:

```shell
mkdir -p data
curl -o data/car_data.csv https://raw.githubusercontent.com/chandanverma07/DataSets/master/car%20data.csv
```

> Для пересохранения интерактивного графика в PNG библиотеке `kaleido` нужен браузер
> на движке Chromium. Если он не установлен, выполните `plotly_get_chrome`.
> Сам блокнот при этом читается и без него — графики уже сохранены в `./eda/`.

# Структура проекта

```
.
|__ data/                            исходные и обработанные данные (не коммитятся)
|    |__ car_data.csv                исходный датасет
|    |__ clean_data.pkl              очищенная выборка
|__ eda/
|    |__ eda.ipynb                   блокнот с разведочным анализом
|    |__ price_scatter.html          интерактивный график (plotly)
|    |__ *.png                       сохранённые графики
|__ .gitignore
|__ README.md
|__ requirements.txt
```

# Исследование данных

В работе.
