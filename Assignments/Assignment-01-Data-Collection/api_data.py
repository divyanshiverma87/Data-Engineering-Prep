import json
import requests


API_URL = "https://jsonplaceholder.typicode.com/users"


def fetch_users():
    """Fetch user data from the API."""
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        print("Error fetching users:", error)
        return []


def process_users(users):
    """Extract required information from API response."""
    processed_users = []

    for user in users:
        user_data = {
            "name": user.get("name", ""),
            "username": user.get("username", ""),
            "email": user.get("email", ""),
            "company": user.get("company", {}).get("name", "")
        }

        processed_users.append(user_data)

    return processed_users


def save_users(users):
    """Save processed users to users.json."""
    with open("users.json", "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4)


def main():
    users = fetch_users()

    if not users:
        print("No user data available.")
        return

    processed_users = process_users(users)

    print("Total Users:", len(processed_users))

    print("\nUser Data:")
    for user in processed_users:
        print(user)

    print("\nCompany Names:")
    for user in processed_users:
        print(user["company"])

    save_users(processed_users)

    print("\nusers.json created successfully!")


if __name__ == "__main__":
    main()