import duckdb


def build_clean_table(db_path: str) -> None:
    """
    Создает очищенную таблицу sales_clean на основе sales_raw.

    Делает:
    - переименование колонок
    - приведение типов
    - нормализацию дат
    - нормализацию текста
    """
    con = duckdb.connect(db_path)

    try:
        # удаляем старую clean-таблицу
        con.execute("DROP TABLE IF EXISTS sales_clean")

        # создаем новую clean-таблицу
        con.execute(
            """
            CREATE TABLE sales_clean AS
            SELECT
                -- приведение к integer
                CAST("Sale ID" AS INTEGER) AS sale_id,

                -- переименование
                "Customer Name" AS customer_name,

                -- приведение к числу
                CAST(Amount AS DOUBLE) AS amount,

                -- обработка разных форматов даты
                COALESCE(
                    TRY_CAST("Sale Date" AS DATE),
                    TRY_STRPTIME("Sale Date", '%Y/%m/%d')::DATE,
                    TRY_STRPTIME("Sale Date", '%d-%m-%Y')::DATE
                ) AS sale_date,

                -- нормализация регистра города
                UPPER(LEFT(City, 1)) || LOWER(SUBSTR(City, 2)) AS city,

                -- приводим канал к нижнему регистру
                LOWER(Channel) AS channel

            FROM sales_raw
            """
        )

    finally:
        con.close()


if __name__ == "__main__":
    build_clean_table("db/loader.duckdb")
