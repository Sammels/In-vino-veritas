import datetime
import argparse
import logging.config
import pandas as pd
from settings import logger_config
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape

logger = logging.getLogger("main_logger")


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


def get_wine(filepath):
    wines_df = pd.read_excel(filepath).fillna("")
    wines_df.rename(
        columns={
            "Категория": "category",
            "Название": "name",
            "Сорт": "type",
            "Цена": "price",
            "Картинка": "picture",
            "Акция": "promo",
        },
        inplace=True,
    )

    wines = wines_df.to_dict(orient="records")
    wines_by_category = defaultdict(list)
    for wine in wines:
        wines_by_category[wine["category"]].append(wine)
    wines_by_category = dict(sorted(wines_by_category.items()))
    return wines_by_category


def create_parser():
    parser = argparse.ArgumentParser(
        prog="Site about new Russian wine",
        description="The script allows you to start "
        "site to sell wines. It shows the information about you wines.",
    )
    parser.add_argument(
        "-p",
        "--path",
        help="You can specify the path to your data file",
        default="wine.xlsx",
    )
    return parser


def main():
    logging.config.dictConfig(logger_config)
    parser = create_parser()
    args = parser.parse_args()

    env = Environment(
        loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
    )

    template = env.get_template("template.html")

    year_now = datetime.datetime.now().year
    vinestart = year_now - 1920
    logger.debug(correct_ends(vinestart))

    rendered_page = template.render(
        vine_start=vinestart,
        ending=correct_ends(vinestart),
        wines_by_category=get_wine(args.path),
    )

    with open("index.html", "w", encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(("0.0.0.0", 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
