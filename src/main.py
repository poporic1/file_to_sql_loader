from pathlib import Path

from load_raw import load_raw_csv
from inspect_table import inspect_table
from build_clean_table import build_clean_table
from profile_table import profile_table
from export_parquet import export_to_parquet


DB_PATH = "db/loader.duckdb"
CSV_PATH = "data/sales_raw.csv"
RAW_TABLE = "sales_raw"
CLEAN_TABLE = "sales_clean"

PROFILE_PATH = "output/profile_report.csv"
PARQUET_PATH = "output/sales_clean.parquet"
SUMMARY_PATH = "output/summary.txt"


def ensure_directories() -> None:
    """Создает папки db и output, если их нет."""
    Path("db").mkdir(exist_ok=True)
    Path("output").mkdir(exist_ok=True)


def save_summary(row_count: int) -> None:
    """Сохраняет краткую информацию о выполнении."""
    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        f.write("File-to-SQL Loader summary\n")
        f.write(f"Raw table: {RAW_TABLE}\n")
        f.write(f"Clean table: {CLEAN_TABLE}\n")
        f.write(f"Row count: {row_count}\n")
        f.write(f"Profile report: {PROFILE_PATH}\n")
        f.write(f"Parquet file: {PARQUET_PATH}\n")


def main() -> None:
    """Основной сценарий выполнения проекта."""
    ensure_directories()

    # 1. загрузка CSV
    load_raw_csv(DB_PATH, CSV_PATH, RAW_TABLE)

    # 2. проверка raw-таблицы
    columns, row_count_df, preview = inspect_table(DB_PATH, RAW_TABLE)

    print("=== RAW COLUMNS ===")
    print(columns)

    print("\n=== RAW ROW COUNT ===")
    print(row_count_df)

    print("\n=== RAW PREVIEW ===")
    print(preview)

    # 3. создание clean-таблицы
    build_clean_table(DB_PATH)

    # 4. profiling
    profile_df = profile_table(DB_PATH, CLEAN_TABLE)
    profile_df.to_csv(PROFILE_PATH, index=False)

    # 5. экспорт в parquet
    export_to_parquet(DB_PATH, CLEAN_TABLE, PARQUET_PATH)

    # 6. summary
    row_count = int(row_count_df["cnt"].iloc[0])
    save_summary(row_count)

    print("\nГотово.")
    print(f"Profiling saved to: {PROFILE_PATH}")
    print(f"Parquet saved to: {PARQUET_PATH}")
    print(f"Summary saved to: {SUMMARY_PATH}")


if __name__ == "__main__":
    main()
