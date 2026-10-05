import json
import requests
from bs4 import BeautifulSoup


URL = "https://books.toscrape.com/"

RATING_VALUES = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}


def fetch_webpage():
    """Fetch the books webpage."""
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        return response.text

    except requests.RequestException as error:
        print("Error fetching webpage:", error)
        return None


def scrape_books(html):
    """Extract book title, price, and rating."""
    soup = BeautifulSoup(html, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    book_data = []

    for book in books:
        title_tag = book.h3.a
        price_tag = book.find("p", class_="price_color")
        rating_tag = book.find("p", class_="star-rating")

        if not title_tag or not price_tag or not rating_tag:
            continue

        title = title_tag.get("title", "").strip()

        price_text = price_tag.get_text(strip=True)
        price_text = price_text.replace("Â£", "").replace("£", "").strip()

        try:
            price = float(price_text)
        except ValueError:
            continue

        rating_name = rating_tag.get("class", [None, None])[1]

        if rating_name not in RATING_VALUES:
            continue

        rating = RATING_VALUES[rating_name]

        book_data.append({
            "title": title,
            "price": price,
            "rating": rating
        })

    return book_data


def analyze_prices(book_data):
    """Calculate book price statistics."""
    if not book_data:
        return None

    most_expensive = max(book_data, key=lambda book: book["price"])
    least_expensive = min(book_data, key=lambda book: book["price"])
    average_price = sum(book["price"] for book in book_data) / len(book_data)

    return {
        "most_expensive": most_expensive,
        "least_expensive": least_expensive,
        "average_price": round(average_price, 2)
    }


def save_books(book_data):
    """Save scraped data to books.json."""
    with open("books.json", "w", encoding="utf-8") as file:
        json.dump(book_data, file, indent=4)


def main():
    html = fetch_webpage()

    if html is None:
        return

    book_data = scrape_books(html)

    if len(book_data) < 20:
        print(f"Error: Only {len(book_data)} books were scraped.")
        print("At least 20 books are required.")
        return

    print("\nBook Data:\n")

    for book in book_data:
        print(book)

    price_analysis = analyze_prices(book_data)

    print("\n--- Price Analysis ---")

    print("Most Expensive Book:")
    print(
        price_analysis["most_expensive"]["title"],
        "£",
        price_analysis["most_expensive"]["price"]
    )

    print("\nLeast Expensive Book:")
    print(
        price_analysis["least_expensive"]["title"],
        "£",
        price_analysis["least_expensive"]["price"]
    )

    print("\nAverage Book Price:")
    print(price_analysis["average_price"])

    save_books(book_data)

    print("\nbooks.json created successfully!")


if __name__ == "__main__":
    main()