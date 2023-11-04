import datetime
import argparse
import logging.config
from settings import logger_config
from collections import defaultdict

from http.server import HTTPServer, SimpleHTTPRequestHandler
from pprint import pprint

logging.config.dictConfig(logger_config)
logger = logging.getLogger("main_logger")

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader("."),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

year_now = datetime.datetime.now().year
vinestart = year_now - 1920


def correct_ends(year):
    """Функция выводит корректное окончание.

    Функция принимает год, и в зависимости от числа ставит верное окончание.

    Args:
        year (int): Дата основания винодельни

    Returns:
        str: Возвращает верное окончание.
    """

    ends = ""
    if year == 100 or year == 111:
        ends = "лет"
    elif year == 101:
        ends = "год"
    elif year == 102:
        ends = "года"
    else:
        ends = "года"
    return ends

logger.debug(correct_ends(vinestart))


wines_df = pd.read_excel('wine2.xlsx').fillna('')
wines_df.rename(columns={'Категория': 'category', 'Название': 'name', 'Сорт': 'type', 'Цена': 'price', 'Картинка': 'picture'}, inplace=True)
wines = wines_df.to_dict(orient='records')
wines_by_category = defaultdict(list)
for wine in wines:
    wines_by_category[wine['category']].append(wine)
wines_by_category = dict(sorted(wines_by_category.items()))


rendered_page = template.render(
    vine_start=vinestart,
    ending=correct_ends(vinestart),
    wines_by_category=wines_by_category,
)

with open('index.html', 'w', encoding='utf8') as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
