# Data Engineering Practice: ETL & Data Cleaning

Учебный репозиторий по дата-инжинирингу. Проект демонстрирует базовые архитектурные паттерны построения ETL-пайплайнов на чистом Python и PostgreSQL.

## Структура проекта

* `coffee_pipeline.py` — изолированный модуль очистки и валидации данных (**Transform Layer**):
  * Валидация входных структур без внешних зависимостей.
  * Паттерн **Guard Clauses** (ранний выход через `continue`).
  * Реализация **Dead Letter Queue (DLQ)** — маршрутизация брака с сохранением исходной записи и точной причины сбоя.
  * Нормализация строковых данных (`.strip()`, `.upper()`) и быстрый поиск по белому списку через `set`.
* `main.py` — сквозной ETL-пайплайн с пакетной загрузкой валидных строк в базу данных (**Load Layer**) через `psycopg2.extras.execute_values`.
* `reader.py` — отказоустойчивое извлечение данных (**Extract Layer**) с изоляцией сетевых сбоев через `try-except`.
* `snippets.py` — шпаргалка по архитектурным паттернам, транзакциям и синтаксису Python.

## Как запустить

1. Клонировать репозиторий:
   ```bash
   git clone [https://github.com/xeniya-kharissova/data-engineering-practice.git](https://github.com/xeniya-kharissova/data-engineering-practice.git)