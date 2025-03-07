from datetime import datetime
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler
import pandas as pd
import numpy
import configargparse
from jinja2 import Environment, FileSystemLoader, select_autoescape


def read_wine_data(file_path):
    """Чтение данных о винах из Excel-файла."""
    wine_dataframe = pd.read_excel(
        file_path,
        sheet_name="Лист1"
    ).replace({numpy.nan: None})
    return wine_dataframe.to_dict(orient='records')


def group_wines_by_category(wine_records):
    wines_by_category = defaultdict(list)

    for record in wine_records:
        category = record['Категория']
        wines_by_category[category].append({
            "image": f"images/{record['Картинка']}",
            "title": record['Название'],
            "sort": record['Сорт'],
            "price": record['Цена'],
            "category": record['Категория'],
            "action": record['Акция']
        })
    return wines_by_category


def calculate_winery_age():
    """Возвращает возраст винодельни и правильное склонение слова 'год'."""
    founding_year = 1920
    current_year = datetime.now().year
    winery_age = current_year - founding_year
    format_years = 'лет' if 11 <= winery_age % 100 <= 14 else (
        {1: 'год', 2: 'года', 3: 'года', 4: 'года'}.get(winery_age % 10, 'лет')
    )
    return winery_age, format_years


def main():
    """Основная функция для генерации HTML-страницы."""
    parser = configargparse.ArgumentParser(
        default_config_files=['config.ini'],
        description="Программа генерирует HTML-страницу с винами из Excel"
    )
    parser.add_argument(
        "--path",
        type=str,
        help="Путь до Excel-файла с данными о винах (по умолчанию wine.xlsx)",
        default="wine.xlsx"
    )
    args, _ = parser.parse_known_args()
    file_path = args.path

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    try:
        wine_records = read_wine_data(file_path)
        wines_by_category = group_wines_by_category(wine_records)
        winery_age, format_years = calculate_winery_age()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Файл '{file_path}' не найден.") from e
    except ValueError as e:
        if "Excel file format cannot be determined" in str(e):
            raise ValueError("Формат файла не Excel.") from e
        if "Worksheet named 'Лист1' not found" in str(e):
            raise ValueError("'Лист1' в Excel файле не найден.") from e

    rendered_page = template.render(
        winery_age=winery_age,
        format_years=format_years,
        wines_by_category=wines_by_category
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
