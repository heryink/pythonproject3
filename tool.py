from anthropic.types import ToolParam
import requests
from bs4 import BeautifulSoup as bs, BeautifulSoup
import csv
import pandas as pd

def scrape_web(url):
    response = requests.get(url=url)
    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.text, "html.parser")
            books = soup.find_all("article", attrs={"class": "product_pod"})
        except Exception as e:
            print(f'An Error occured:{e}')


    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

    with open("books.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Title", "Price", "Rating"])
        for book in books:
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text
            rating = rating_map[(book.find("p")["class"][1])]
            writer.writerow([title, price, rating])

    with open("books.csv", "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        ratings = list(reader)
        print(ratings)

    data = pd.read_csv("books.csv")
    return data.to_json(orient="records")

scrape_web_schema = ToolParam({
    "name" : "scrape_web",
    "description" : "Scrape the name,rating and price of books in the url provided and return data extracted from web pages in the format specified",
    "input_schema": {
        "type": "object",
        "required": ["url"],
        "properties": { "url": {
        "type": "string",
        "description": "The URL of the web page to scrape"
    }
}      }
})


scrape_web("https://books.toscrape.com/")
