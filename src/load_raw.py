import duckdb


def load_raw_csv(db_path: str, csv_path: str, table_name: str) -> None:
    """
    Загружает CSV-файл в DuckDB как таблицу.

    Параметры:
    db_path: путь к файлу базы данных
    csv_path: путь к CSV-файлу
    table_name: имя создаваемой таблицы
    """
    # подключение к базе
    con = duckdb.connect(db_path)

    try:
        # удаляем таблицу, если уже существует
        con.execute(f"DROP TABLE IF EXISTS {table_name}")

        # создаем таблицу из CSV
        con.execute(
            f"""
            CREATE TABLE {table_name} AS
            SELECT *
            FROM read_csv_auto('{csv_path}', header=True)
            """
        )
    finally:
        # закрываем соединение
        con.close()


if __name__ == "__main__":
    load_raw_csv("db/loader.duckdb", "data/sales_raw.csv", "sales_raw")
