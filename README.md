# Python-Library-Project
This is a Project from UTH class 'Python Programmig'

This project is a comprehensive Library Management System developed using Python and the Pandas library. It provides functionalities for both users and administrators to manage books, accounts, and orders in a library. The system includes:

### Key Features

- **User Account Management**: Users can create accounts, log in, and manage their personal details, including password updates and account balance adjustments.
- **Book Management**: Administrators can add, update, and delete book entries. Users can view available books, add books to their favorites, and place orders.
- **Review and Rating System**: Users can add, view, and delete reviews for books they have purchased.
- **Order Management**: Users can manage their orders, including placing new orders and viewing past orders.
- **Favorites and Recommendations**: Users can add books to their favorites list and receive recommendations based on their favorite categories.
- **CSV Integration**: The system supports CSV file uploads and downloads for easy data management.

### Installation

To get started with the Library Management System, clone the repository and install the required dependencies:

```bash
git clone https://github.com/your-username/library-management-system.git
cd library-management-system
pip install -r requirements.txt
```

### Usage

The system is designed for ease of use, with a clear distinction between user and admin functionalities. Users can register, log in, and explore the library's offerings, while admins have full control over the system's data.

---

**DETAILED CODE REPORT**   
All questions are answered below, and I have listed all the functions for easier access:

- **initialize_dataframes()**: This code initializes three different dataframes for managing user, admin, and book data using the pandas library. It first defines the columns for each dataframe (user_columns, admin_columns, books_columns). It then checks for the existence of the CSV files that contain the user, admin, and book data. This allows dynamic initialization of data depending on the availability of the CSV files.

- **save_dataframes()**: Designed to save three different dataframes (users, admins, and books) into CSV files. If the save is successful, the message "Data saved successfully." is displayed.

- **validate_username()**: The function `validate_username(username)` checks if the provided username does not already exist in the `username` column of `user_df`.

- **validate_password()**: The function `validate_password(password)` ensures that a password meets two critical criteria: it is at least 8 characters long and includes at least one special character from a specified list.

- **create_user_account()**: The function `create_user_account()` prompts the user to enter a unique username and a secure password, validating their validity. It then collects user information such as address, city, and initial balance, creates a new user in the database, and confirms the account creation.

- **validate_admin_username()** and **validate_admin_password()**: The functions `validate_admin_username(username)` check if a username is unique in `admin_df`, while `validate_admin_password(password)` ensures the password is at least 8 characters long.

- **admin_login()**: The function `admin_login()` allows an admin to log into the system by entering their username and password. It checks the validity of these credentials in the `admin_df` database and displays corresponding success or failure messages. If failed login attempts reach three, the program terminates for security reasons.

- **user_login()**: Allows a user to log into the system by entering their username and password. It searches for the username in the database and verifies the user's identity via the password. On successful login, it allows the user to proceed to the menu. On failure, it increases the number of failed attempts and terminates the program if attempts reach three.

- **view_books()**: Allows the user to view the available books in the system. It starts by printing the title "Available Books:" and checks if `books_df` is empty. If no books are available, it prints the message "No books available." If books are available, it prints the details for each book, including the title, author, publisher, categories, price, shipping cost, availability, and the number of copies. It also checks and prints any reviews for each book, indicating the user number, rating, and comment. The function includes checks to ensure the correct storage and display of data to avoid issues such as incorrect review formatting or empty book categories.

- **add_book()**: Allows an admin to add a new book to the database. Initially, the admin is prompted to enter the basic book details, such as title, author, publisher, and categories, which are stored in the variables title, author, publisher, and categories. The categories are entered separated by commas and converted into a list using the `split(',')` method. The admin then enters the book's cost and shipping cost, which are stored in the variables cost and shipping_cost as float objects. The availability of the book is then entered as True or False.

- **delete_book_entry()**: Allows an admin to delete a book from the database. It first asks the user to enter the ID of the book they want to delete. It then checks if the book exists in the database and if the admin has access to the store where the book is registered. If all is well, the book is deleted, and the changes are saved in the database.

- **update_book()**: Allows an admin to update the details of a book in the database. It prompts the user to enter the book ID they want to update, checks its existence, and confirms that the admin has access to the store where the book is registered. The admin can then update the book's data, such as title, author, publisher, categories, cost, shipping cost, availability, and copies.

- **add_review()**: Works as follows:
  - The user is asked to enter the `book_id` of the book they wish to review and the rating for the book from 1 to 5 (`rating`).
  - The function checks if the entered rating is within the range of 1 to 5. If not, the user is asked to enter a new rating until a valid value is provided.
  - The user is then prompted to enter a comment for their review (`comment`).
  - The function checks if the `book_id` exists in the user's order list identified by `user_id`. This ensures that only users who have purchased the book can review it.
  - If the review is permissible, a review entry (`review_entry`) is created in the form of a dictionary with the fields:
    - `user_id`: The user's ID who is making the review.
    - `rating`: The rating given by the user.
    - `comment`: The comment added by the user.
  - The review is added to the `reviews` list of the specific book in the `books_df` DataFrame.
  - If the `reviews` column does not yet exist (e.g., it is the first review for this book), it is created as an empty list.

- **admin_menu()**: Provides a menu of options for the administrators.

- **upload_books_from_csv()**: Loads new books from a CSV file into the library system. It reads each line of the CSV, checks if each book already exists in the library based on its title, and if not, adds it. Finally, it saves the changes to the CSV and displays confirmation messages as the task progresses.

- **user_menu()**: Provides a menu of options for the users.

- **check_account_balance()**: The function `check_account_balance(user_id)` is used to return the balance of a user's account based on the user_id. It simply retrieves the balance from the `user_df` DataFrame using the `at` method, displaying the result in decimal form.

- **remove_from_favorites()**: Used to remove a book from a user's favorites list. The user is prompted to enter the ID of the book they want to remove. The function checks if the book exists in the user's favorites list and, if so, removes it and saves the changes. If the book is not found in the favorites list, a corresponding message is displayed.

- **check_favorites_availability()**: Used to check the availability and price of the books added to a user's favorites list. It searches the user's favorites book list, checks availability, and calculates the total price (book price + shipping cost) for each. If a book is unavailable or not found in the books_df database, a corresponding message is displayed.

- **view_orders()**: Used to display the user's orders. It first searches the user's order list in the `user_df` DataFrame. If there are no orders, the user is asked if they wish to place a new order. If the answer is yes, the function `place_order(user_id, book_id)` is called to place a new order. If there are orders, the details of each order, such as the book title and total price (book price + shipping cost), are displayed. The user can then add a new order, remove an existing one, or do nothing.

- **remove_review()**: Concerns the deletion of a review from a book in the `books_df` DataFrame. The user enters the book ID, and if there are reviews for it, they are displayed with a corresponding index number. The user selects the review number they wish to delete. The review is deleted from the `books_df` and the changes are saved.

- **delete_order()**: The function `delete_order(user_id, book_id)` allows users to remove book orders from their list. During its execution, it checks if the specific book is in the user's orders, and if so, removes it from the order list, returning the cost of the book to the user's balance. It also increases the number of available book copies and the inventory count in the warehouses.

- **add_individual_entries()**: Offers users three basic functions and an option to return to the main menu.
  - Add Book to Favorites: Users can add a book to their favorites list.
  - Place Order: Users can place an order for a specific book.
  - Adjust Balance: Users can adjust their account balance, increasing or decreasing it as per their choice.

- **add_to_favorites()**: Adds a book to a user's favorites list. It first checks if the book is not already in the list. If it is not, it is added and the changes are saved.

- **place_order()**: Allows users to place orders for books in the system. It checks if the book exists and if it has not already been ordered by the user.

- **recommend_books()**: Provides book recommendations for a user based on their favorite books in a specific category. Let's analyze its operation step by step:
  - First, it retrieves the user's favorite book list ('favorites') from the `user_df` DataFrame.
  - If there are no favorite books for the user, it prints a message and terminates the function.
  - It creates a dictionary ('category_counts') to count the occurrences of each category in the user's favorite books.
  - It finds the category with the most occurrences in the

 user's favorites list. If there is a tie between categories, the one with the smallest index is selected.
  - Finally, it displays book recommendations based on the selected category with the most occurrences. If there are no books in this category, a corresponding message is displayed.

- **withdraw_balance()**: Allows users to withdraw money from their account. It first prompts the user to enter the desired withdrawal amount and then checks if the amount is less than or equal to their current balance. If the amount is valid, it deducts the amount from the user's balance and prints a confirmation message.

- **admin_menu_option()**: The `admin_menu_option()` function is used to call the `admin_menu()` function, providing an entry point for administrators into the administrative system menu.

- **calculate_discount()**: The `calculate_discount` function calculates the total discount for a user's orders based on a discount percentage. The user enters the discount percentage (0 to 100), which is divided by 100 to convert it to a decimal form, and then multiplies it by the total order cost, rounding to two decimal places.

---

