import json

# Load JSON files
with open("users.json", "r") as file:
    users = json.load(file)

with open("books.json", "r") as file:
    books = json.load(file)


# ==============================
# USER ANALYSIS
# ==============================

print("========== USER ANALYSIS ==========")

# Total Users
total_users = len(users)
print("Total Users:", total_users)


# Unique Companies
companies = set(user["company"] for user in users)

print("Unique Companies:", len(companies))


# Top 5 Companies Alphabetically
top_5_companies = sorted(companies)[:5]

print("\nTop 5 Companies Alphabetically:")

for company in top_5_companies:
    print(company)


# ==============================
# BOOK ANALYSIS
# ==============================

print("\n========== BOOK ANALYSIS ==========")

# Average Price
average_price = sum(book["price"] for book in books) / len(books)

print("Average Price: £", round(average_price, 2))


# Highest Rated Books
highest_rating = max(book["rating"] for book in books)

print("\nHighest Rated Books:")

for book in books:
    if book["rating"] == highest_rating:
        print(book["title"])


# Number of Books in Each Rating Category
rating_count = {}

for book in books:
    rating = book["rating"]

    if rating in rating_count:
        rating_count[rating] += 1
    else:
        rating_count[rating] = 1


print("\nNumber of Books in Each Rating Category:")

for rating in sorted(rating_count):
    print("Rating", rating, ":", rating_count[rating], "books")


# ==============================
# SUMMARY
# ==============================

print("\n========== SUMMARY ==========")

print("Total Users:", total_users)
print("Unique Companies:", len(companies))
print("Total Books:", len(books))
print("Average Book Price: £", round(average_price, 2))
print("Highest Rating:", highest_rating)