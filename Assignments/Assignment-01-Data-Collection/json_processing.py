import json


USERS_FILE = "users.json"
BOOKS_FILE = "books.json"
REPORT_FILE = "report.json"


def load_json(filename):
    """Load and return data from a JSON file."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        print(f"Error: {filename} was not found.")
        return None

    except json.JSONDecodeError:
        print(f"Error: {filename} contains invalid JSON.")
        return None


def find_high_rated_books(books):
    """Return books with a rating greater than 4."""
    return [
        book for book in books
        if book.get("rating", 0) > 4
    ]


def find_group_users(users):
    """Return users whose company name contains 'Group'."""
    return [
        user for user in users
        if "Group" in user.get("company", "")
    ]


def calculate_average_price(books):
    """Calculate the average price of books."""
    if not books:
        return 0

    prices = [
        book.get("price", 0)
        for book in books
    ]

    return round(sum(prices) / len(prices), 2)


def create_report(users, books, high_rated_books, group_users):
    """Create a combined report from users and books data."""
    return {
        "user_summary": {
            "total_users": len(users),
            "group_company_users": [
                {
                    "name": user["name"],
                    "company": user["company"]
                }
                for user in group_users
            ]
        },

        "book_summary": {
            "total_books": len(books),
            "average_price": calculate_average_price(books),
            "high_rated_books": [
                {
                    "title": book["title"],
                    "rating": book["rating"]
                }
                for book in high_rated_books
            ]
        }
    }


def save_report(report):
    """Save the combined report to report.json."""
    with open(REPORT_FILE, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)


def main():
    users = load_json(USERS_FILE)
    books = load_json(BOOKS_FILE)

    if users is None or books is None:
        print("Unable to process the data.")
        return

    if not isinstance(users, list) or not isinstance(books, list):
        print("Error: JSON data must contain lists.")
        return

    print("Total Users:", len(users))
    print("Total Books:", len(books))

    high_rated_books = find_high_rated_books(books)

    print("\nBooks with Rating Greater Than 4:")
    for book in high_rated_books:
        print(book["title"])

    group_users = find_group_users(users)

    print("\nUsers belonging to companies containing 'Group':")
    for user in group_users:
        print(user["name"], "-", user["company"])

    report = create_report(
        users,
        books,
        high_rated_books,
        group_users
    )

    save_report(report)

    print("\nreport.json created successfully!")


if __name__ == "__main__":
    main()