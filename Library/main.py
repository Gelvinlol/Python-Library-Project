import pandas as pd
import ast
import os
import re
import csv
import matplotlib.pyplot as plt


# Initialize DataFrames
def initialize_dataframes():
    global user_df, admin_df, books_df

    user_columns = ['id', 'username', 'password', 'address', 'city', 'orders', 'favorites', 'balance']
    admin_columns = ['id', 'username', 'password', 'bookstores']
    books_columns = ['id', 'title', 'author', 'publisher', 'categories', 'cost', 'shipping_cost', 'availability',
                     'copies', 'bookstores', 'reviews']

    if os.path.exists('users.csv'):
        user_df = pd.read_csv('users.csv', converters={'orders': ast.literal_eval, 'favorites': ast.literal_eval,
                                                       'reviews': lambda x: ast.literal_eval(x) if pd.notna(x) else []})
    else:
        user_df = pd.DataFrame(columns=user_columns)

    if os.path.exists('admins.csv'):
        admin_df = pd.read_csv('admins.csv', converters={'bookstores': ast.literal_eval})
    else:
        admin_df = pd.DataFrame(columns=admin_columns)

    if os.path.exists('books.csv'):
        books_df = pd.read_csv('books.csv', converters={'categories': ast.literal_eval, 'bookstores': ast.literal_eval})
    else:
        books_df = pd.DataFrame(columns=books_columns)


def save_dataframes():
    try:
        user_df.to_csv('users.csv', index=False)
        admin_df.to_csv('admins.csv', index=False)
        books_df.to_csv('books.csv', index=False)
        print("Data saved successfully.")
    except PermissionError as e:
        print(f"Error: {e}")
        print("Please ensure you have write permissions and the file is not open in another program.")


# User validation
def validate_username(username):
    return username not in user_df['username'].values


def validate_password(password):
    return len(password) >= 8 and re.search(r'[!@#$%^&*(),.?":{}|<>]', password) is not None


# User account creation
def create_user_account():
    global user_df
    username = input("Enter a unique username: ")
    while not validate_username(username):
        print("Username already exists or is invalid.")
        username = input("Enter a unique username: ")

    password = input("Enter a password (at least 8 characters and one special character): ")
    while not validate_password(password):
        print("Password does not meet the requirements.")
        password = input("Enter a password (at least 8 characters and one special character): ")

    address = input("Enter your address: ")
    city = input("Enter your city: ")
    balance = float(input("Enter your starting balance: "))

    new_user = {
        'id': len(user_df) + 1,
        'username': username,
        'password': password,
        'address': address,
        'city': city,
        'orders': [],
        'favorites': [],
        'balance': balance
    }

    user_df = user_df.append(new_user, ignore_index=True)
    save_dataframes()
    print("User account created successfully!")


# Admin validation
def validate_admin_username(username):
    return username not in admin_df['username'].values


def validate_admin_password(password):
    return len(password) >= 8


failed_attempts = 0


# Admin login
def admin_login():
    global failed_attempts
    username = input("Enter your admin username: ")
    password = input("Enter your admin password: ")

    if (admin_df['username'] == username).any() and (admin_df['password'] == password).any():
        print(f"Welcome, {username}! You are logged in as an admin.")
        admin_menu(username)
        failed_attempts = 0
    else:
        failed_attempts += 1
        if failed_attempts >= 3:
            print("Three failed attempts. Exiting the program.")
            exit()
        print("Invalid admin username or password.")


# User login
def user_login():
    global failed_attempts
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    try:
        # Try to find the user based on username
        user_row = user_df[user_df['username'] == username]
        if not user_row.empty:  # Check if any user was found
            user_id = user_row['id'].values[0]
            if user_row['password'].values[0] == password:
                print(f"Welcome, {username}! You are logged in as a user.")
                print(user_id)
                user_menu(user_id)
                failed_attempts = 0
            else:
                print("Invalid password.")
                failed_attempts += 1
        else:
            print("Username not found.")
            failed_attempts += 1
    except IndexError:  # Handle potential indexing error if user not found
        print("Username not found..")
        failed_attempts += 1

    if failed_attempts >= 3:
        print("Three failed attempts. Exiting the program.")
        exit()


# View books
def view_books():
    global books_df, user_df

    print("\nAvailable Books:")
    if books_df.empty:
        print("No books available.")
    else:
        for index, row in books_df.iterrows():
            print(f"Book ID: {row['id']}")
            print(f"Title: {row['title']}")
            print(f"Author: {row['author']}")
            print(f"Publisher: {row['publisher']}")
            categories = row['categories']
            if isinstance(categories, str):
                categories = ast.literal_eval(categories)  # Convert categories string to list
            print(f"Categories: {categories}")
            print(f"Cost: ${row['cost']}")
            print(f"Shipping Cost: ${row['shipping_cost']}")
            print(f"Availability: {row['availability']}")
            print(f"Copies: {row['copies']}")
            print("Reviews:")

            if pd.notna(row['reviews']):
                try:
                    reviews = ast.literal_eval(row['reviews'])
                    if isinstance(reviews, list):
                        for review in reviews:
                            print(
                                f"User ID: {review['user_id']}, Rating: {review['rating']}, Comment: {review['comment']}")
                    else:
                        print("Error: Reviews should be stored as a list of dictionaries.")
                except ValueError:
                    print("Error: Reviews format is invalid.")
            else:
                print("No reviews yet.")

            print("-" * 30)



# Add book
def add_book(admin_username):
    global books_df
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    publisher = input("Enter book publisher: ")
    categories = input("Enter book categories (comma separated): ").split(',')
    cost = float(input("Enter book cost: "))
    shipping_cost = float(input("Enter shipping cost: "))
    availability = input("Enter book availability (True/False): ").lower() == 'true'
    copies = int(input("Enter number of copies: "))

    admin_row = admin_df[admin_df['username'] == admin_username]
    admin_bookstores = admin_row['bookstores'].values[0]

    bookstores = {}
    for store in admin_bookstores:
        store_copies = int(input(f"Enter number of copies at {store}: "))
        bookstores[store] = store_copies

    if books_df[books_df['title'] == title].empty:
        new_book = {
            'id': len(books_df) + 1,
            'title': title,
            'author': author,
            'publisher': publisher,
            'categories': categories,
            'cost': cost,
            'shipping_cost': shipping_cost,
            'availability': availability,
            'copies': copies,
            'bookstores': bookstores,
        }
        books_df = books_df.append(new_book, ignore_index=True)
        save_dataframes()
        print("Book added successfully!")
    else:
        print("Book already exists. Use the update functionality.")


def delete_book_entry(admin_username):
    global books_df, admin_df

    try:
        # Get the book ID to delete
        book_id = int(input("Enter the Book ID to delete: "))

        # Check if the book ID exists in the library
        if book_id not in books_df['id'].values:
            print(f"Book ID {book_id} does not exist in the library.")
            return

        # Get the admin's bookstores
        admin_row = admin_df[admin_df['username'] == admin_username]
        admin_bookstores = admin_row['bookstores'].values[0]

        # Convert admin_bookstores from list of IDs to list of store names
        admin_store_names = [f"Store {store_id}" for store_id in admin_bookstores]

        # Get the bookstores where the book is listed
        book_row = books_df[books_df['id'] == book_id]
        book_bookstores = eval(book_row.iloc[0]['bookstores']) if isinstance(book_row.iloc[0]['bookstores'], str) else \
            book_row.iloc[0]['bookstores']
        # ================================================== Mporoume na to kanoume kai etsi gia pio apla
        # book_bookstores = book_row.iloc[0]['bookstores']
        # if isinstance(book_bookstores, str):
        #     book_bookstores = eval(book_bookstores)

        # Check if the admin has access to any of the bookstores where the book is listed
        if not any(store in admin_store_names for store in book_bookstores):
            print("You do not own any of the bookstores where this book is listed. Deletion not allowed.")
            return

        # If access is granted, delete the book entry
        books_df = books_df[books_df['id'] != book_id]
        print(f"Book ID {book_id} has been successfully deleted.")
        save_dataframes()

    except Exception as e:
        print(f"Error: {e}")


# Update book
def update_book(admin_username):
    global books_df
    book_id = int(input("Enter the book ID to update: "))
    book_row = books_df[books_df['id'] == book_id]

    if book_row.empty:
        print("Book ID not found.")
        return

    # Get the admin's bookstores
    admin_row = admin_df[admin_df['username'] == admin_username]
    admin_bookstores = admin_row['bookstores'].values[0]

    # Convert admin_bookstores from list of IDs to list of store names
    admin_store_names = [f"Store {store_id}" for store_id in admin_bookstores]

    # Check if the admin owns any of the bookstores where the book is listed
    book_bookstores = book_row.iloc[0]['bookstores']
    print(book_bookstores)
    if not any(store in admin_store_names for store in book_bookstores):
        print("You do not own any of the bookstores where this book is listed. Update not allowed.")
        return

    # Proceed with updating the book
    print("Enter new book details:")
    title = input("Enter new book title: ")
    author = input("Enter new book author: ")
    publisher = input("Enter new book publisher: ")
    categories = input("Enter new book categories (comma separated): ").split(',')
    cost = float(input("Enter new book cost: "))
    shipping_cost = float(input("Enter new shipping cost: "))
    availability = input("Enter new book availability (True/False): ").lower() == 'true'
    copies = int(input("Enter new number of copies: "))

    # Update the book details in the dataframe
    books_df.loc[books_df['id'] == book_id, 'title'] = title
    books_df.loc[books_df['id'] == book_id, 'author'] = author
    books_df.loc[books_df['id'] == book_id, 'publisher'] = publisher
    books_df.loc[books_df['id'] == book_id, 'categories'] = categories
    books_df.loc[books_df['id'] == book_id, 'cost'] = cost
    books_df.loc[books_df['id'] == book_id, 'shipping_cost'] = shipping_cost
    books_df.loc[books_df['id'] == book_id, 'availability'] = availability
    books_df.loc[books_df['id'] == book_id, 'copies'] = copies
    save_dataframes()
    print("Book updated successfully!")


# Add review
def add_review(user_id):
    global user_df, books_df

    book_id = int(input("Enter the book ID to review: "))
    rating = int(input("Enter your rating (1-5): "))

    while rating < 1 or rating > 5:
        rating = int(input("Invalid rating. Enter your rating (1-5): "))

    comment = input("Enter your review comment: ")

    # Check if book_id is in user's orders
    user_orders = user_df.at[user_id - 1, 'orders']  # Assuming user_id is 1-based index
    if book_id not in user_orders:
        print("You can only review books that you have ordered.")
        return

    # Construct review entry
    review_entry = {
        'user_id': user_id,
        'rating': rating,
        'comment': comment
    }

    # Append review to books_df
    if 'reviews' not in books_df.columns:
        books_df['reviews'] = [[] for _ in range(len(books_df))]

    books_index = books_df.index[books_df['id'] == book_id].tolist()[0]
    books_reviews = books_df.at[books_index, 'reviews']

    if not isinstance(books_reviews, list):
        books_reviews = ast.literal_eval(books_reviews) if pd.notna(books_reviews) else []

    books_reviews.append(review_entry)
    books_df.at[books_index, 'reviews'] = books_reviews

    # Save DataFrame to CSV
    books_df.to_csv('books.csv', index=False)  # Ensure index=False to avoid extra commas

    print("Review and comment added successfully!")

# Admin functions
def admin_menu(username):
    while True:
        print("\nAdmin Menu")
        print("1. View Books")
        print("2. Upload Books from CSV")
        print("3. Add Book")
        print("4. Update Book")
        print("5. Generate Reports")
        print("6. Export Books to CSV")
        print("7. Check Book Availability by Title")
        print("8. Check Book Availability by Title and Store")
        print("9. Calculate Book Cost")
        print("10. Calculate Total Cost of Available Books ανά εκδότη/συγγραφέα/συνολικά")
        print("11. Delete User by Username")
        print("12. Delete Book")
        print("13. Remove Review")
        print("14. Logout")
        choice = input("Enter your choice: ")

        if choice == '1':
            view_books()
        elif choice == '2':
            file_path = input("Enter the path to the CSV file: ")
            upload_books_from_csv(file_path)
        elif choice == '3':
            add_book(username)
        elif choice == '4':
            update_book(username)
        elif choice == '5':
            generate_reports()
        elif choice == '6':
            export_books_to_csv()
        elif choice == '7':
            check_book_availability_by_title()
        elif choice == '8':
            check_book_availability_by_title_and_store()
        elif choice == '9':
            calculate_book_cost()
        elif choice == '10':
            calculate_total_cost_of_available_books()
        elif choice == '11':
            delete_user_by_username()
        elif choice == '12':
            delete_book_entry(username)
        elif choice == '13':
            remove_review()
        elif choice == '14':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")


def upload_books_from_csv(file_path):
    global books_df

    # Read the CSV file into a DataFrame
    new_books_df = pd.read_csv(file_path)

    # Iterate through each row in the new books DataFrame
    for index, new_book in new_books_df.iterrows():
        # Check if the book ID already exists in books_df
        if new_book['title'] in books_df['title'].values:
            # If the book exists, print a message and do not update
            print(f"Book ID {new_book['id']} ({new_book['title']}) already exists. Skipping update.")
        else:
            # If the book does not exist, append it to books_df
            books_df = pd.concat([books_df, pd.DataFrame([new_book])], ignore_index=True)
            print(f"Added new book ID {new_book['id']}: {new_book['title']}")

    print("Book information has been successfully uploaded.")
    save_dataframes()


# User functions
def user_menu(user_id):
    while True:
        print("\nUser Menu")
        print("1. View Books")
        print("2. Add Review")
        print("3. Upload Favorites from CSV")
        print("4. Add individual entries")
        print("5. Change Personal Information")
        print("6. Remove from Favorites")
        print("7. Check Account Balance")
        print("8. Check Favorites Availability and Price")
        print("9. View your orders")
        print("10. Get Book Recommendation")
        print("11. Logout")
        choice = input("Enter your choice: ")

        if choice == '1':
            view_books()
        elif choice == '2':
            add_review(user_id)
        elif choice == '3':
            path = input("Enter the path to the CSV file: ")
            upload_favorites_csv(user_id, path)
        elif choice == '4':
            add_individual_entries(user_id)
        elif choice == '5':
            select_Change(user_id)
        elif choice == '6':
            remove_from_favorites(user_id)
        elif choice == '7':
            check_account_balance(user_id)
        elif choice == '8':
            check_favorites_availability(user_id)
        elif choice == '9':
            view_orders(user_id)
        elif choice == '10':
            recommend_books(user_id)
        elif choice == '11':
            print("Logging out...")
            main()
            break
        else:
            print("Invalid choice. Please try again.")


def check_account_balance(user_id):
    global user_df

    try:
        balance = user_df.at[user_id - 1, 'balance']
        print(f"\nYour account balance is: ${balance:.2f}")

    except Exception as e:
        print(f"Error: {e}")


# Function to remove book from favorites
def remove_from_favorites(user_id):
    global user_df

    try:
        print("\nRemove Book from Favorites")
        book_id = int(input("Enter the book ID to remove from favorites: "))

        if book_id in user_df.at[user_id - 1, 'favorites']:
            user_df.at[user_id - 1, 'favorites'].remove(book_id)
            save_dataframes()
            print(f"Book ID {book_id} removed from favorites successfully.")
        else:
            print(f"Book ID {book_id} is not in your favorites list.")

    except ValueError:
        print("Invalid input. Please enter a valid book ID.")
    except Exception as e:
        print(f"Error: {e}")


def check_favorites_availability(user_id):
    global user_df, books_df

    try:
        favorites = user_df.loc[user_df['id'] == user_id, 'favorites'].values[0]

        if not favorites:
            print("No favorite books found.")
            return

        print("\nFavorites Availability and Price Check")
        for book_id in favorites:
            book = books_df.loc[books_df['id'] == book_id]

            if not book.empty:
                book_title = book.iloc[0]['title']
                book_price = book.iloc[0]['cost']
                book_price += book.iloc[0]['shipping_cost']
                book_availability = book.iloc[0]['availability']
                availability_text = "Available" if book_availability else "Not Available"
                print(
                    f"Book ID: {book_id}, Title: {book_title}, Price+Shipping: ${book_price:.2f}, Availability: {availability_text}")

    except Exception as e:
        print(f"Error: {e}")


def view_orders(user_id):
    global user_df, books_df

    try:
        orders = user_df.loc[user_df['id'] == user_id, 'orders'].values[0]

        if not orders:
            print("No orders found.")
            ask = input("Do you want to place an order? (Yes/No) ").strip()
            while ask not in ['Yes', 'No']:
                print("Only 'Yes' or 'No'")
                ask = input("Do you want to place an order? (Yes/No) ").strip()
            if ask == 'Yes':
                book_id = int(input("Enter the book ID you want to order: "))
                place_order(user_id, book_id)
            return

        print("\nYour Orders")
        for book_id in orders:
            book = books_df.loc[books_df['id'] == book_id]

            if not book.empty:
                book_title = book.iloc[0]['title']
                book_price = book.iloc[0]['cost']
                book_price += book.iloc[0]['shipping_cost']
                print(f"Book ID: {book_id}, Title: {book_title}, Price+Shipping: ${book_price:.2f}")

        ask = input(
            "Do you want to (1) Add a new order, (2) Remove an order, or (3) Do nothing? Enter 1, 2, or 3: ").strip()
        while ask not in ['1', '2', '3']:
            print("Only '1', '2', or '3'")
            ask = input(
                "Do you want to (1) Add a new order, (2) Remove an order, or (3) Do nothing? Enter 1, 2, or 3: ").strip()
        if ask == '1':
            book_id = int(input("Enter the book ID you want to order: "))
            place_order(user_id, book_id)
        elif ask == '2':
            book_id = int(input("Enter Book ID you wish to remove: "))
            delete_order(user_id, book_id)

    except Exception as e:
        print(f"Error: {e}")


def remove_review():
    global books_df

    book_id = int(input("Enter the Book ID to remove a review: "))
    books_index = books_df.index[books_df['id'] == book_id].tolist()[0]

    if pd.notna(books_df.at[books_index, 'reviews']):
        reviews = ast.literal_eval(books_df.at[books_index, 'reviews'])

        if reviews:
            print("Current Reviews:")
            for i in range(len(reviews)):
                review = reviews[i]
                print(
                    f"{i + 1}. User ID: {review['user_id']}, Rating: {review['rating']}, Comment: {review['comment']}")

            review_index = int(input("Enter the index of the review to remove(Not the UserID): ")) - 1

            if 0 <= review_index < len(reviews):
                reviews.pop(review_index)
                books_df.at[books_index, 'reviews'] = str(reviews)
                print("Review removed successfully.")
                save_dataframes()
            else:
                print("Invalid review index.")
        else:
            print("No reviews found for this book.")
    else:
        print("No reviews found for this book.")


def delete_order(user_id, book_id):
    try:
        orders = user_df.loc[user_df['id'] == user_id, 'orders'].values[0]
        if book_id in orders:
            orders.remove(book_id)
            user_df.at[user_df[user_df['id'] == user_id].index[0], 'orders'] = orders

            book_price = books_df.loc[books_df['id'] == book_id, 'cost'].values[0]
            book_price += books_df.loc[books_df['id'] == book_id, 'shipping_cost'].values[0]
            user_df.loc[user_df['id'] == user_id, 'balance'] += book_price

            # Increment the general copies column
            books_df.loc[books_df['id'] == book_id, 'copies'] += 1

            # Increment the count in the bookstores dictionary
            bookstores = books_df.loc[books_df['id'] == book_id, 'bookstores'].values[0]
            for store, count in bookstores.items():
                bookstores[store] += 1
                break

            save_dataframes()
            print(
                f"Book ID {book_id} has been removed from your orders. ${book_price:.2f} has been refunded to your "f"balance.")
        else:
            print(f"Book ID {book_id} is not in your orders.")

    except Exception as e:
        print(f"Error: {e}")


def add_individual_entries(user_id):
    while True:
        print("\nAdd individual Entries:")
        print("1. Add Book to Favorites")
        print("2. Place Order")
        print("3. Adjust Balance")
        print("4. Back to User Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            book_id = input("Enter the ID of the book to add to favorites: ")
            add_to_favorites(user_id, int(book_id))
        elif choice == '2':
            book_id = input("Enter the ID of the book to order: ")
            place_order(user_id, int(book_id))
        elif choice == '3':
            amount = float(input("Enter the amount to adjust balance (positive for increase, negative for decrease): "))
            adjust_balance(user_id, amount)
        elif choice == '4':
            print("Returning to User Menu...")
            break
        else:
            print("Invalid choice. Please try again.")


def add_to_favorites(user_id, book_id):
    global user_df
    if book_id not in user_df.at[user_id - 1, 'favorites']:
        user_df.at[user_id - 1, 'favorites'].append(book_id)
        save_dataframes()
        print("Book added to favorites successfully!")
    else:
        print("Book is already in favorites.")


def place_order(user_id, book_id):
    global user_df, books_df
    if book_id in books_df['id'].values:
        if book_id not in user_df.at[user_id - 1, 'orders']:
            user_df.at[user_id - 1, 'orders'].append(book_id)
            book_price = books_df.loc[books_df['id'] == book_id, 'cost'].values[0]
            book_price += books_df.loc[books_df['id'] == book_id, 'shipping_cost'].values[0]
            user_df.at[user_id - 1, 'balance'] -= book_price
            # Remove one copy from the store
            bookstores = books_df.loc[books_df['id'] == book_id, 'bookstores'].values[0]
            for store, count in bookstores.items():
                if count > 0:
                    bookstores[store] -= 1
                    break
            # Decrement the general copies column
            books_df.loc[books_df['id'] == book_id, 'copies'] -= 1
            save_dataframes()
            print("Order placed successfully!")
        else:
            print("You have already ordered this book.")
    else:
        print("Book ID does not exist.")


def recommend_books(user_id):
    # Retrieve the list of favorite book IDs for the given user
    favorites = user_df.loc[user_df['id'] == user_id, 'favorites'].values[0]

    # If the user has no favorite books, print a message and exit the function
    if not favorites:
        print("No favorite books found for recommendations.")
        return

    # Initialize an empty dictionary to count the occurrences of each category in the favorite books
    category_counts = {}

    # Iterate over each favorite book ID
    for book_id in favorites:
        # Retrieve the book information from books_df for the current book_id
        book = books_df.loc[books_df['id'] == book_id]

        # Evaluate the string representation of the categories list to convert it to an actual list
        categories = eval(str(book.iloc[0]['categories']))

        # Iterate over each category in the list
        for category in categories:
            # Increment the category count in the dictionary, or initialize it if not already present
            if category in category_counts:
                category_counts[category] += 1
            else:
                category_counts[category] = 1

    # If no categories were found in the favorite books, print a message and exit the function
    if not category_counts:
        print("No categories found in favorite books for recommendations.")
        return

    # Find the category with the highest count (most common category)
    most_common_category = max(category_counts, key=category_counts.get)

    # Retrieve the list of order book IDs for the given user
    orders = user_df.loc[user_df['id'] == user_id, 'orders'].values[0]

    # Create a set of book IDs that are either in favorites or orders to exclude them from recommendations
    excluded_books = set(favorites) | set(orders)

    # Filter the books_df to find books that are not in the excluded_books set and belong to the most common category
    possible_recommendations = books_df[
        (books_df['id'].apply(lambda x: x not in excluded_books)) &  # Exclude books in favorites and orders
        (books_df['categories'].apply(lambda x: most_common_category in eval(str(x))))
        # Include books in the most common category
        ]

    # If no possible recommendations are found, print a message
    if possible_recommendations.empty:
        print(f"No new recommendations available for the category '{most_common_category}'.")
    else:
        # Randomly select up to 3 books from the possible recommendations
        recommendations = possible_recommendations.sample(n=min(3, len(possible_recommendations))).iloc

        # Print the recommended books
        print(f"\nRecommended Books based on your favorites in the category '{most_common_category}':")
        for recommendation in recommendations:
            print(
                f"Book ID: {recommendation['id']}, Title: {recommendation['title']}, Price: ${recommendation['cost']:.2f}")


def adjust_balance(user_id, amount):
    global user_df
    user_df.at[user_id - 1, 'balance'] += amount
    save_dataframes()
    print(f"Balance adjusted by {amount}.")


def upload_favorites_csv(user_id, file_path):
    global user_df, books_df

    try:
        # Read the CSV file
        favorites_data = pd.read_csv(file_path)

        # Extract book IDs as a list
        favorite_books = favorites_data['book_id'].tolist()

        # Validate and update favorites for the user
        if user_id <= len(user_df):
            current_favorites = user_df.at[user_id - 1, 'favorites']  # Assuming user_id is 1-based index
            new_favorites = list(set(current_favorites + favorite_books))  # Ensure no duplicates

            # Update the favorites column in user_df
            user_df.at[user_id - 1, 'favorites'] = new_favorites

            # Save the updated DataFrame
            save_dataframes()

            print("Favorites updated successfully!")
        else:
            print(f"User with ID {user_id} not found.")

    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"Error: {e}")


def modify_personal_details(user_id, field_to_change, new_value):
    try:
        if user_id <= len(user_df):
            # Update the user details based on the chosen field
            if field_to_change.lower() == 'username':
                user_df.at[user_id - 1, 'username'] = new_value
            elif field_to_change.lower() == 'password':
                user_df.at[user_id - 1, 'password'] = new_value
            elif field_to_change.lower() == 'address':
                user_df.at[user_id - 1, 'address'] = new_value
            elif field_to_change.lower() == 'city':
                user_df.at[user_id - 1, 'city'] = new_value
            else:
                print("Invalid field name. Please choose from 'Username', 'Password', 'Address', or 'City'.")

            # Save the updated DataFrame
            save_dataframes()

            print(f"{field_to_change.capitalize()} updated successfully!")
        else:
            print(f"User with ID {user_id} not found.")

    except Exception as e:
        print(f"Error: {e}")


def select_Change(user_id):
    print("What would you like to change?")
    print("1. Username")
    print("2. Password")
    print("3. Address")
    print("4. City")
    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        new_username = input("Enter new username: ")
        modify_personal_details(user_id, 'username', new_username)
    elif choice == '2':
        new_password = input("Enter new password: ")
        modify_personal_details(user_id, 'password', new_password)
    elif choice == '3':
        new_address = input("Enter new address: ")
        modify_personal_details(user_id, 'address', new_address)
    elif choice == '4':
        new_city = input("Enter new city: ")
        modify_personal_details(user_id, 'city', new_city)
    else:
        print("Invalid choice. Please enter a number between 1 and 4.")


# Generate Reports
def generate_reports():
    while True:
        print("\nGenerate Reports")
        print("1. Number of Books by Publisher (considering availability)")
        print("2. Number of Books by Publisher (not considering availability)")
        print("3. Number of Books by Author (considering availability)")
        print("4. Number of Books by Author (not considering availability)")
        print("5. Number of Books by Category (considering availability)")
        print("6. Number of Books by Store (considering availability)")
        print("7. Distribution of Available Book Costs")
        print("8. Number of Users by City")
        print("9. Back to Admin Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            books_by_publisher(consider_availability=True)
        elif choice == '2':
            books_by_publisher(consider_availability=False)
        elif choice == '3':
            books_by_author(consider_availability=True)
        elif choice == '4':
            books_by_author(consider_availability=False)
        elif choice == '5':
            books_by_category(consider_availability=True)
        elif choice == '6':
            books_by_store()
        elif choice == '7':
            distribution_of_book_costs()
        elif choice == '8':
            users_by_city()
        elif choice == '9':
            break
        else:
            print("Invalid choice. Please try again.")


def books_by_publisher(consider_availability=True):
    if consider_availability:
        df = books_df[books_df['availability']]
    else:
        df = books_df
    publisher_counts = df['publisher'].value_counts()

    plt.figure(figsize=(10, 6))
    publisher_counts.plot(kind='bar')
    plt.title('Number of Books by Publisher')
    plt.xlabel('Publisher')
    plt.ylabel('Number of Books')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


def books_by_author(consider_availability=True):
    if consider_availability:
        df = books_df[books_df['availability']]
    else:
        df = books_df
    author_counts = df['author'].value_counts()

    plt.figure(figsize=(10, 6))
    author_counts.plot(kind='bar')
    plt.title('Number of Books by Author')
    plt.xlabel('Author')
    plt.ylabel('Number of Books')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


def books_by_category(consider_availability=True):
    if consider_availability:
        df = books_df[books_df['availability']]
    else:
        df = books_df
    category_counts = df.explode('categories')['categories'].value_counts()

    plt.figure(figsize=(10, 6))
    category_counts.plot(kind='bar')
    plt.title('Number of Books by Category')
    plt.xlabel('Category')
    plt.ylabel('Number of Books')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


def books_by_store():
    store_counts = {}

    for bookstores in books_df['bookstores']:
        for store, count in bookstores.items():
            if store in store_counts:
                store_counts[store] += count
            else:
                store_counts[store] = count

    store_series = pd.Series(store_counts)

    plt.figure(figsize=(10, 6))
    store_series.plot(kind='bar')
    plt.title('Number of Books by Store')
    plt.xlabel('Store')
    plt.ylabel('Number of Books')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


def distribution_of_book_costs():
    df = books_df[books_df['availability']]
    costs = df['cost']

    plt.figure(figsize=(10, 6))
    plt.hist(costs, bins=10, edgecolor='k')
    plt.title('Distribution of Available Book Costs')
    plt.xlabel('Cost')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()


def users_by_city():
    city_counts = user_df['city'].value_counts()

    plt.figure(figsize=(10, 6))
    city_counts.plot(kind='bar')
    plt.title('Number of Users by City')
    plt.xlabel('City')
    plt.ylabel('Number of Users')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


# Export books to CSV
def export_books_to_csv():
    books_df.to_csv('exported_books.csv', index=False)
    print("Books exported to 'exported_books.csv' successfully.")


# Check book availability by title
def check_book_availability_by_title():
    title = input("Enter book title to check availability: ")
    available_books = books_df[(books_df['title'].str.contains(title, case=False)) & (books_df['availability'])]

    if not available_books.empty:
        print(f"Books available for title '{title}':")
        for index, row in available_books.iterrows():
            print(f"Book ID: {row['id']}, Title: {row['title']}, Copies: {row['copies']}")
    else:
        print(f"No available books found for title '{title}'.")


# Check book availability by title and store
def check_book_availability_by_title_and_store():
    title = input("Enter book title to check availability: ")
    store_name = input("Enter store name to check availability: ")
    available_books = books_df[(books_df['title'].str.contains(title, case=False)) & (books_df['availability'])]

    if not available_books.empty:
        found = False
        for index, row in available_books.iterrows():
            if store_name in row['bookstores']:
                found = True
                print(
                    f"Book ID: {row['id']}, Title: {row['title']}, Store: {store_name}, Copies: {row['bookstores'][store_name]}")
        if not found:
            print(f"No available books found for title '{title}' in store '{store_name}'.")
    else:
        print(f"No available books found for title '{title}'.")


# Calculate book cost (cost + shipping cost)
def calculate_book_cost():
    book_id = int(input("Enter the book ID to calculate cost: "))
    book = books_df[books_df['id'] == book_id]

    if not book.empty:
        total_cost = book['cost'].values[0] + book['shipping_cost'].values[0]
        print(f"Total cost of book ID {book_id}: ${total_cost}")
    else:
        print(f"No book found with ID {book_id}.")


# Calculate total cost of available books by publisher/author/total
def calculate_total_cost_of_available_books():
    print("Calculate Total Cost of Available Books")
    print("1. By Publisher")
    print("2. By Author")
    print("3. Total")
    choice = input("Enter your choice: ")

    if choice == '1':
        publisher = input("Enter publisher name: ")
        books = books_df[(books_df['publisher'].str.contains(publisher, case=False)) & (books_df['availability'])]
        total_cost = (books['cost'] + books['shipping_cost']).sum()
        print(f"Total cost of available books by publisher '{publisher}': ${total_cost}")
    elif choice == '2':
        author = input("Enter author name: ")
        books = books_df[(books_df['author'].str.contains(author, case=False)) & (books_df['availability'])]
        total_cost = (books['cost'] + books['shipping_cost']).sum()
        print(f"Total cost of available books by author '{author}': ${total_cost}")
    elif choice == '3':
        total_cost = (books_df[books_df['availability']]['cost'] + books_df[books_df['availability']][
            'shipping_cost']).sum()
        print(f"Total cost of all available books: ${total_cost}")
    else:
        print("Invalid choice. Please try again.")


# Delete user by username
def delete_user_by_username():
    global user_df  # Ensure we modify the global variable

    username = input("Enter username of the user to delete: ")

    if username in user_df['username'].values:
        user_df = user_df[user_df['username'] != username]
        save_dataframes()
        print(f"User '{username}' deleted successfully.")
    else:
        print(f"User '{username}' not found.")


# Main function to run the program
def main():
    initialize_dataframes()

    print("Welcome to the Library Management System!")
    print("1. User Login")
    print("2. Admin Login")
    print("3. Create User Account")
    print("4. Exit")

    while True:
        choice = input("Enter your choice: ")

        if choice == '1':
            user_login()
        elif choice == '2':
            admin_login()
        elif choice == '3':
            create_user_account()
        elif choice == '4':
            print("Exiting the program.")
            exit()
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
