import json


USERS_FILE = "users.json"
BOOKS_FILE = "books.json"


def load_json(filename):
    """Load data from a JSON file."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        print(f"Error: {filename} was not found.")
        return None

    except json.JSONDecodeError:
        print(f"Error: {filename} contains invalid JSON.")
        return None


def analyze_users(users):
    """Analyze user and company data."""
    total_users = len(users)

    companies = {
        user.get("company", "")
        for user in users
        if user.get("company")
    }

    top_5_companies = sorted(companies)[:5]

    return {
        "total_users": total_users,
        "unique_companies": len(companies),
        "top_5_companies": top_5_companies
    }


def analyze_books(books):
    """Analyze book price and rating data."""
    if not books:
        return {
            "average_price": 0,
            "highest_rating": 0,
            "highest_rated_books": [],
            "rating_count": {}
        }

    prices = [
        book.get("price", 0)
        for book in books
    ]

    average_price = sum(prices) / len(prices)

    highest_rating = max(
        book.get("rating", 0)
        for book in books
    )

    highest_rated_books = [
        book["title"]
        for book in books
        if book.get("rating", 0) == highest_rating
    ]

    rating_count = {}

    for book in books:
        rating = book.get("rating")

        if rating is not None:
            rating_count[rating] = rating_count.get(rating, 0) + 1

    return {
        "average_price": round(average_price, 2),
        "highest_rating": highest_rating,
        "highest_rated_books": highest_rated_books,
        "rating_count": rating_count
    }


def display_analysis(user_analysis, book_analysis, total_books):
    """Display the analysis results."""

    print("========== USER ANALYSIS ==========")

    print("Total Users:", user_analysis["total_users"])
    print("Unique Companies:", user_analysis["unique_companies"])

    print("\nTop 5 Companies Alphabetically:")
    for company in user_analysis["top_5_companies"]:
        print(company)

    print("\n========== BOOK ANALYSIS ==========")

    print("Total Books:", total_books)
    print("Average Price: £", book_analysis["average_price"])

    print("\nHighest Rated Books:")
    for title in book_analysis["highest_rated_books"]:
        print(title)

    print("\nNumber of Books in Each Rating Category:")

    for rating in sorted(book_analysis["rating_count"]):
        count = book_analysis["rating_count"][rating]
        print(f"Rating {rating}: {count} books")

    print("\n========== SUMMARY ==========")

    print("Total Users:", user_analysis["total_users"])
    print("Unique Companies:", user_analysis["unique_companies"])
    print("Total Books:", total_books)
    print("Average Book Price: £", book_analysis["average_price"])
    print("Highest Rating:", book_analysis["highest_rating"])


def main():
    users = load_json(USERS_FILE)
    books = load_json(BOOKS_FILE)

    if users is None or books is None:
        print("Unable to perform analysis.")
        return

    if not isinstance(users, list) or not isinstance(books, list):
        print("Error: JSON data must contain lists.")
        return

    user_analysis = analyze_users(users)
    book_analysis = analyze_books(books)

    display_analysis(
        user_analysis,
        book_analysis,
        len(books)
    )


if __name__ == "__main__":
    main()