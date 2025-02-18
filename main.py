from datetime import datetime
import pandas as pd
import numpy
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape


def read_wine_data(file_path):
    """Чтение данных о винах из Excel-файла."""
    try:
        df = pd.read_excel(file_path, sheet_name="Лист1").replace({numpy.nan: None})
        return df.to_dict(orient='records')
    except FileNotFoundError:
        raise ValueError(f"Файл {file_path} не найден!"
                         f"Файл должен быть 'wine3.xlsx', лист 'Лист1'.")
    except Exception as e:
        raise ValueError(f"Ошибка при чтении файла: {e}")


def group_wines_by_category(wine_records):
    categories = {record['Категория'] for record in wine_records}
    wines_by_category = defaultdict(list)

    for category in categories:
        for record in wine_records:
            if record['Категория'] == category:
                wines_by_category[category].append({
                    "image": f"images/{record['Картинка']}",
                    "title": record['Название'],
                    "sort": record['Сорт'],
                    "price": record['Цена'],
                    "category": record['Категория'],
                    "action": record['Акция']
                })
    return wines_by_category


def calculate_winery_age(founding_year):
    """Вычисление возраста винодельни."""
    current_year = datetime.now().year
    winery_age = current_year - founding_year
    format_years = 'лет' if 11 <= winery_age % 100 <= 14 else (
        {1: 'год', 2: 'года', 3: 'года', 4: 'года'}.get(winery_age % 10, 'лет')
    )
    return winery_age, format_years


def main():
    """Основная функция для генерации HTML-страницы."""
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    wine_records = read_wine_data("wine3.xlsx")
    wines_by_category = group_wines_by_category(wine_records)

    winery_age, format_years = calculate_winery_age(1920)

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
