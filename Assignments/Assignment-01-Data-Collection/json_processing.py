import json

# Load users.json
with open("users.json", "r") as file:
    users = json.load(file)

# Load books.json
with open("books.json", "r") as file:
    books = json.load(file)


# Task C1: Total records
print("Total Users:", len(users))
print("Total Books:", len(books))


# Task C2: Books with rating greater than 4
print("\nBooks with Rating Greater Than 4:")

for book in books:
    if book["rating"] > 4:
        print(book["title"])


# Task C3: Users belonging to companies containing "Group"
print("\nUsers belonging to companies containing 'Group':")

for user in users:
    if "Group" in user["company"]:
        print(user["name"], "-", user["company"])


# Task C4: Create combined report
average_price = sum(book["price"] for book in books) / len(books)

report = {
    "total_users": len(users),
    "total_books": len(books),
    "average_price": round(average_price, 2)
}


# Save report.json
with open("report.json", "w") as file:
    json.dump(report, file, indent=4)

print("\nreport.json created successfully!")