import duckdb


def inspect_table(db_path: str, table_name: str):
    """
    Возвращает информацию о таблице:
    - структуру колонок
    - количество строк
    - первые записи

    Параметры:
    db_path: путь к базе
    table_name: имя таблицы
    """
    con = duckdb.connect(db_path)

    try:
        # структура колонок
        columns = con.execute(f"DESCRIBE {table_name}").fetchdf()

        # количество строк
        row_count = con.execute(f"SELECT COUNT(*) AS cnt FROM {table_name}").fetchdf()

        # первые 5 строк
        preview = con.execute(f"SELECT * FROM {table_name} LIMIT 5").fetchdf()

        return columns, row_count, preview

    finally:
        con.close()


if __name__ == "__main__":
    columns, row_count, preview = inspect_table("db/loader.duckdb", "sales_raw")

    print("=== COLUMNS ===")
    print(columns)

    print("\n=== ROW COUNT ===")
    print(row_count)

    print("\n=== PREVIEW ===")
    print(preview)
