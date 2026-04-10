import re


def normalize_column_name(name: str) -> str:
    """
    Приводит имя колонки к стандартному виду:
    - нижний регистр
    - пробелы и символы - underscore
    - убирает лишние "_"
    """
    # убираем пробелы по краям и переводим в нижний регистр
    name = name.strip().lower()

    # заменяем всё, кроме букв и цифр, на "_"
    name = re.sub(r"[^a-z0-9]+", "_", name)

    # убираем повторяющиеся "_"
    name = re.sub(r"_+", "_", name)

    # убираем "_" в начале и конце
    return name.strip("_")


if __name__ == "__main__":
    test_columns = [
        "Sale ID",
        "Customer Name",
        "Sale Date",
        "Amount",
        "City",
        "Channel",
    ]

    for column in test_columns:
        print(column, "->", normalize_column_name(column))
