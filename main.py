import requests
from bs4 import BeautifulSoup
import json

headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "3600",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
}

url = f"https://tailwindcss.com/docs/customizing-colors"

colors_list = []

req = requests.get(url, headers)

soup = BeautifulSoup(req.content, "html.parser")


def get_color_list(soup: BeautifulSoup):
    list_items = soup.find(id="content-wrapper").find("div", "grid").children
    for index, item in enumerate(list_items):
        category = item.div.get_text()
        color_codes = []
        colors = item.find_next("div", "grid").children
        for index, color in enumerate(colors):
            color_text = color.div.find("div", "px-0.5").get_text().split("#")
            color_codes.append(
                {
                    "id": index,
                    "label": color_text[0],
                    "code": f"#{color_text[1]}"
                }
            )
        colors_list.append({"category": category, "colors": color_codes})


def save_as_json(dictionary_list):
    with open("tailwind.json", "w") as outfile:
        json.dump(dictionary_list, outfile, ensure_ascii=False, indent=2)


get_color_list(soup)
save_as_json(colors_list)
