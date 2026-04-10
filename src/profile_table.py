import duckdb
import pandas as pd


def profile_table(db_path: str, table_name: str) -> pd.DataFrame:
    """
    Строит profiling-отчет по таблице.

    Для каждой колонки считает:
    - тип
    - количество строк
    - количество NULL
    - количество уникальных значений
    - min / max / avg
    """
    con = duckdb.connect(db_path)

    try:
        columns = con.execute(f"DESCRIBE {table_name}").fetchall()
        rows = []

        # общее количество строк
        total_rows = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]

        for col_name, col_type, *_ in columns:

            # считаем NULL
            null_count = con.execute(
                f'SELECT COUNT(*) FROM {table_name} WHERE "{col_name}" IS NULL'
            ).fetchone()[0]

            # считаем уникальные значения
            distinct_count = con.execute(
                f'SELECT COUNT(DISTINCT "{col_name}") FROM {table_name}'
            ).fetchone()[0]

            row = {
                "column_name": col_name,
                "data_type": col_type,
                "row_count": total_rows,
                "null_count": null_count,
                "distinct_count": distinct_count,
            }

            # считаем числовые метрики только для числовых колонок
            if col_type.upper() in ("INTEGER", "BIGINT", "DOUBLE", "DECIMAL"):
                min_value, max_value, avg_value = con.execute(
                    f'SELECT MIN("{col_name}"), MAX("{col_name}"), AVG("{col_name}") FROM {table_name}'
                ).fetchone()

                row["min_value"] = min_value
                row["max_value"] = max_value
                row["avg_value"] = avg_value

            rows.append(row)

        return pd.DataFrame(rows)

    finally:
        con.close()


if __name__ == "__main__":
    df = profile_table("db/loader.duckdb", "sales_clean")
    print(df)
