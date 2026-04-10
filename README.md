# File-to-SQL Loader

Локальный инструмент для загрузки CSV-файла в базу данных DuckDB, приведения данных к нормальному виду и формирования базового profiling-отчёта.

## Задача проекта

В реальной работе данные часто приходят в виде CSV-файлов с разными проблемами:

- разные форматы дат
- пустые значения
- разный регистр текста
- неудобные названия колонок

Цель проекта - быстро превратить такой файл в нормальную SQL-таблицу, с которой можно работать дальше.

---

## Что делает утилита

Проект выполняет следующие шаги:

1. Загружает CSV в DuckDB как raw-таблицу
2. Создаёт clean-таблицу:

   - приводит названия колонок
   - приводит типы данных
   - нормализует даты
   - нормализует текстовые значения
3. Строит profiling-отчёт по таблице
4. Сохраняет результат в Parquet

---

## Структура проекта

```
file_to_sql_loader/
│
├── data/
│   └── sales_raw.csv
│
├── db/
│   └── loader.duckdb
│
├── output/
│   ├── profile_report.csv
│   ├── sales_clean.parquet
│   └── summary.txt
│
├── src/
│   ├── load_raw.py
│   ├── inspect_table.py
│   ├── clean_columns.py
│   ├── build_clean_table.py
│   ├── profile_table.py
│   ├── export_parquet.py
│   └── main.py
│
└── README.md
```
- data/  
Содержит исходные CSV-файлы
-db/  
Файл базы данных DuckDB:
   - sales_raw - исходные данные
   - sales_clean - очищенные данные
- output/  
Результаты работы скрипта:
   - profile_report.csv - profiling таблицы
   - sales_clean.parquet - очищенные данные в формате Parquet
   - summary.txt - краткая сводка выполнения
- src/  
Основная логика проекта:
   - load_raw.py - загрузка CSV в raw-таблицу
   - inspect_table.py - первичный анализ структуры таблицы
   - clean_columns.py - очистка и приведение названий колонок
   - build_clean_table.py - создание clean-таблицы с преобразованиями
   - profile_table.py - расчет статистики по таблице
   - export_parquet.py - экспорт данных в Parquet
   - main.py - точка входа
---

## Установка и запуск

### 1. Установить зависимости

```bash
pip install duckdb pandas
```

---

### 2. Запустить проект

```bash
python src/main.py
```

---

## Входные данные

Файл:
`data/sales_raw.csv`

Пример данных:

```
Sale ID,Customer Name,Amount,Sale Date,City,Channel
1,Ivan Petrov,1000,2026-01-10,Moscow,web
2,Anna Sidorova,2500,2026/01/11,Kazan,store
3,Olga Ivanova,,2026-01-11,SPB,web
```

Особенности:

- разные форматы дат
- пустые значения
- разные регистры текста

---

## Выходные данные

После запуска создаются:

### 1. База данных

```
db/loader.duckdb
```

Содержит:

- `sales_raw`
- `sales_clean`

---

### 2. Profiling-отчёт

```
output/profile_report.csv
```

Содержит:

- количество строк
- количество NULL
- уникальные значения
- min / max / avg для числовых полей

---

### 3. Parquet-файл

```
output/sales_clean.parquet
```

Используется для дальнейшей аналитики.

---

### 4. Summary

```
output/summary.txt
```

Краткая информация о выполнении.

---

## Что происходит с данными

### Raw слой

Данные загружаются как есть.

### Clean слой

Выполняются преобразования:

- `Sale ID` → `sale_id` (INTEGER)
- `Amount` → DOUBLE
- пустые значения → NULL
- даты приводятся к DATE (поддержка нескольких форматов)
- `city` нормализуется:

  - Moscow
  - Kazan
  - Spb
- `channel` приводится к нижнему регистру

---