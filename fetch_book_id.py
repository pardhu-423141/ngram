import requests
from bs4 import BeautifulSoup
import re

URLs = ["https://www.gutenberg.org/ebooks/search/?query=Jane+Austen",
        "https://www.gutenberg.org/ebooks/search/?query=jane+austen&start_index=26",
        "https://www.gutenberg.org/ebooks/search/?query=jane+austen&start_index=51"]
books = {}
for i in range(3):
    response = requests.get(URLs[i], timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    for book in soup.select("li.booklink"):
        link = book.find("a")
        title_tag = book.find("span", class_="title")

        if link and title_tag:
            href = link.get("href", "")
            match = re.search(r"/ebooks/(\d+)", href)

            if match:
                book_id = match.group(1)
                title = title_tag.text.strip()
                books[book_id] = title

with open("jane_austen_book_ids.txt", "w", encoding="utf-8") as f:
    for book_id, title in sorted(books.items()):
        f.write(f"{book_id}\t{title}\n")

print(f"Total books found: {len(books)}")
