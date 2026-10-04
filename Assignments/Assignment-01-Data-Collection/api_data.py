import requests
import json

# API URL
url = "https://jsonplaceholder.typicode.com/users"

# Fetch data from API
response = requests.get(url)

# Convert API response into Python data
users = response.json()

# Task A2: Count total users
print("Total Users:", len(users))

# Task A4: Create processed user data
processed_users = []

for user in users:

    user_data = {
        "name": user["name"],
        "email": user["email"],
        "company": user["company"]["name"]
    }

    processed_users.append(user_data)

# Task A1: Display user information
print("\nUser Data:")

for user in processed_users:
    print(user)

# Task A3: Extract company names
companies = [user["company"] for user in processed_users]

print("\nCompany Names:")

for company in companies:
    print(company)

# Task A5: Save data into users.json
with open("users.json", "w") as file:
    json.dump(processed_users, file, indent=4)

print("\nusers.json created successfully!")