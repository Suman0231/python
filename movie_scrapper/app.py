from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

BASE_URL = "http://quotes.toscrape.com"

def get_all_authors():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    authors = set()

    quotes = soup.find_all("div", class_="quote")
    for quote in quotes:
        author = quote.find("small", class_="author").text
        authors.add(author)

    return sorted(authors)


def get_quotes_by_author(selected_author):
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    quotes_data = []

    quotes = soup.find_all("div", class_="quote")

    for quote in quotes:
        author = quote.find("small", class_="author").text

        if author == selected_author:
            text = quote.find("span", class_="text").text
            tags = [tag.text for tag in quote.find_all("a", class_="tag")]

            quotes_data.append({
                "text": text,
                "author": author,
                "tags": tags
            })

    return quotes_data


@app.route("/", methods=["GET", "POST"])
def index():
    authors = get_all_authors()
    quotes = []
    selected_author = None

    if request.method == "POST":
        selected_author = request.form.get("author")
        quotes = get_quotes_by_author(selected_author)

    return render_template(
        "index.html",
        authors=authors,
        quotes=quotes,
        selected_author=selected_author
    )


if __name__ == "__main__":
    app.run(debug=True)