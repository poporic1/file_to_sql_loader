import duckdb


def export_to_parquet(db_path: str, table_name: str, output_path: str) -> None:
    """
    Экспортирует таблицу из DuckDB в файл Parquet.

    Параметры:
    db_path: путь к базе
    table_name: таблица для экспорта
    output_path: путь к выходному файлу
    """
    con = duckdb.connect(db_path)

    try:
        con.execute(
            f"COPY {table_name} TO '{output_path}' (FORMAT PARQUET)"
        )
    finally:
        con.close()


if __name__ == "__main__":
    export_to_parquet(
        "db/loader.duckdb",
        "sales_clean",
        "output/sales_clean.parquet"
    )