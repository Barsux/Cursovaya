from base import *
import pandas as pd
FILENAME = "table.csv"
DELIMETER = ";"


# Функция считывает csv файл в кодировке UTF-8 с указанным названием и разделителем.
def read_csv(filename, delimeter):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
            lines = list(map(lambda x: x.strip().split(delimeter), lines))
            return lines
    except FileNotFoundError:
        print("Ошибка. Файл не найден.")
    except Exception as e:
        print(f"Ошибка. {e}")
    return


# Фукнция проверяет целостность полученной таблицы, кол-во столбцов и наличие значения хотя бы в одной из строк столбца.
def integrity_checker(lines, length):
    validlines = 0
    for i, line in enumerate(lines):
        if len(line) != length:
            print(f"Ошибка в строке {i + 1}. Неверное количество столбцов.")
            return False
        if all(line):
            validlines += 1
    if validlines == 0:
        print("Ошибка. Один из столбцов таблицы пуст.")
        return False
    return True


# Функция преобразует все значения в таблице к числовому типу, если это возможно.
# Пустые значения заменяются на 0 или "Н/Д".
def reformat_lines(lines):
    val_sample = []
    for line in lines:
        if all(line):
            val_sample = list(map(lambda el: el.isdigit(), line))
            break
    for i in range(len(lines)):
        for j, el in enumerate(lines[i]):
            if not len(el):
                lines[i][j] = 0 if val_sample[j] else "Н/Д"
            else:
                lines[i][j] = int(el) if val_sample[j] else el
    return lines


def main():
    # Считываем csv файл
    lines = read_csv(FILENAME, DELIMETER)
    headers = lines[0]
    lines = lines[1:]

    # Проверяем целостность таблицы
    if not integrity_checker(lines, len(headers)):
        print("Исправьте файл и попробуйте ещё раз.")
        return

    # Преобразуем значения в таблице к числовому типу
    lines = reformat_lines(lines)
    products_amount = len(lines)

    # Создаём таблицу как словарь
    table = {}
    zipped_lines = list(zip(*lines))
    for i, header in enumerate(headers):
        table[header] = zipped_lines[i]

    max_selled_products = find_max_idx(lines, key=lambda x: x[4])
    max_profit_products = find_max_idx(lines, key=lambda x: x[6])


    print("Наибольшее кол-во продаж:")
    for idx in max_selled_products:
        print(f"\tТовар: {table['Название товара'][idx]}, продано: {table['Количество продаж'][idx]}")
    print()

    print("Наибольшая выручка:")
    for idx in max_profit_products:
        print(f"\tТовар: {table['Название товара'][idx]}, выручка: {table['Общая стоимость'][idx]}")
    print()

    # Находим общую выручку
    revenue = sum_by_key(lines, lambda x: x[6])
    print(f'Общая выручка: {revenue}')
    revenue_percent = []

    # Считаем процент выручки для каждого товара с округлением до двух знаков. Временно преобразуем в integer.
    for i in range(products_amount):
        revenue_percent.append((str(round((table['Общая стоимость'][i] / revenue) * 100, 3)) + "%"))
    table['Процент выручки'] = tuple(revenue_percent)

    # Сортируем таблицу по проценту выручки и выводим результат
    sorted_table_idxs, _ = bubble_sort_idx(list(map(lambda val: float(val.replace('%', '')), table["Процент выручки"])))

    # На основе sorted_table_idxs[::-1] создаём dataframe
    df = pd.DataFrame()
    for header in ["Название товара", "Количество продаж", "Процент выручки"]:
        df[header] = [table[header][idx] for idx in sorted_table_idxs[::-1]]

    # Выводим dataframe в консоль
    print("\nТаблица в виде dataframe:")
    print(df.to_string(index=False))

    # Дополнительное задание хз зачем
    # Отсортируем цены по возрастанию
    _, sorted_prices = bubble_sort_idx(list(table["Цена за единицу"]))

    # Цена айфона
    iphone_price = table['Цена за единицу'][0]

    # Найдём эту цену в отсортированном списке
    iphone_price_idx = binary_search(sorted_prices, iphone_price)
    print(f"\nАйфон в списке отсортированных цен находится на {iphone_price_idx + 1} месте.")


if __name__ == "__main__":
    try:
        print("Made in Barsukland!\n")
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print("\nПрограмма завершила работу!")
