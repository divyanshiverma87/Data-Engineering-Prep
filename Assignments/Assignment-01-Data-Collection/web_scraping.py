import requests
import json
from bs4 import BeautifulSoup

# Website URL
url = "https://books.toscrape.com/"

# Fetch webpage
response = requests.get(url)

# Create BeautifulSoup object
soup = BeautifulSoup(response.text, "html.parser")

# Find all books
books = soup.find_all("article", class_="product_pod")

# Store book data
book_data = []

for book in books:

    # Extract title
    title = book.h3.a["title"]

    # Extract and clean price
    price = book.find("p", class_="price_color").text.strip()
    price = price.replace("Â£", "").replace("£", "")
    price = float(price)

    # Extract rating
    rating = book.find("p", class_="star-rating")["class"][1]

    # Convert rating into number
    rating_values = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    rating = rating_values[rating]

    # Create dictionary
    book_info = {
        "title": title,
        "price": price,
        "rating": rating
    }

    book_data.append(book_info)

# Display books
print("\nBook Data:\n")

for book in book_data:
    print(book)

# Task B4: Price Analysis

prices = [book["price"] for book in book_data]

most_expensive = max(book_data, key=lambda x: x["price"])
least_expensive = min(book_data, key=lambda x: x["price"])
average_price = sum(prices) / len(prices)

print("\n--- Price Analysis ---")

print("Most Expensive Book:")
print(most_expensive["title"], "£", most_expensive["price"])

print("\nLeast Expensive Book:")
print(least_expensive["title"], "£", least_expensive["price"])

print("\nAverage Book Price:")
print(round(average_price, 2))



# Task B5: Save book data into books.json
with open("books.json", "w") as file:
    json.dump(book_data, file, indent=4)

print("\nbooks.json created successfully!")