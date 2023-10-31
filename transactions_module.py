import csv
import os
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime

# Initialize NumPy arrays for transactions
transaction_ids = np.array([], dtype=int)
transaction_customer_ids = np.array([], dtype=int)
transaction_dates = np.array([], dtype=str)
transaction_categories = np.array([], dtype=str)
transaction_values = np.array([], dtype=float) 

# Function to generate a random transaction ID
def generate_transaction_id(existing_ids):
    while True:
        transaction_id = np.random.randint(1, 999999)
        if transaction_id not in existing_ids:
            return transaction_id

# Function to add a new transaction
def add_transaction(customer_id, date, category):
    global transaction_ids, transaction_customer_ids, transaction_dates, transaction_categories, transaction_values

    transaction_id = generate_transaction_id(transaction_ids)
    transaction_ids = np.append(transaction_ids, transaction_id)
    transaction_customer_ids = np.append(transaction_customer_ids, customer_id)
    transaction_dates = np.append(transaction_dates, date)
    transaction_categories = np.append(transaction_categories, category)

    transaction = {
        'transaction_id': transaction_id,
        'customer_id': customer_id,
        'date': date,
        'category': category,
    }
    return transaction


# Function to load transaction records from a CSV file and add new records to the memory
def load_transactions_from_csv(file_path):
    global transaction_ids, customer_ids, transaction_dates, transaction_categories

    try:
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if 'transaction_id' in row and 'customer_id' in row and 'date' in row and 'category' in row:
                    transaction_id = int(row['transaction_id'])
                    customer_id = int(row['customer_id'])
                    date = row['date']
                    category = row['category']

                    # Check if the customer exists in memory
                    if customer_id not in customer_ids:
                        print(f"Customer with ID {customer_id} in transaction {transaction_id} does not exist in memory. Skipping this transaction.")
                        continue

                    # Check for duplicate transaction IDs
                    if transaction_id in transaction_ids:
                        print(f"Skipping duplicate transaction ID: {transaction_id}")
                        continue

                    transaction_ids = np.append(transaction_ids, transaction_id)
                    customer_ids = np.append(customer_ids, customer_id)
                    transaction_dates = np.append(transaction_dates, date)
                    transaction_categories = np.append(transaction_categories, category)
                else:
                    print("Skipping row with missing fields (transaction_id, customer_id, date, category).")

        print(f"Transaction records loaded from {file_path}.")
    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print(f"Error: {str(e)}")

# Function to save transaction records to a CSV file with user interaction
def save_transactions_to_csv_with_prompt(file_path):
    if os.path.exists(file_path):
        while True:
            user_input = input(f"The file '{file_path}' already exists. Do you want to (C)ancel, (O)verwrite, or (R)ename it? ").strip().lower()
            if user_input == 'c':
                print("Operation canceled.")
                return
            elif user_input == 'o':
                break
            elif user_input == 'r':
                new_file_path = input("Enter a new file path: ").strip()
                file_path = new_file_path
                if not file_path.endswith(".csv"):
                    file_path += ".csv"
                break
            else:
                print("Invalid input. Please enter 'C', 'O', or 'R'.")

    try:
        with open(file_path, 'w', newline='') as csv_file:
            fieldnames = ['transaction_id', 'customer_id', 'date', 'category']
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()
            for i in range(len(transaction_ids)):
                csv_writer.writerow({'transaction_id': transaction_ids[i], 'customer_id': customer_ids[i], 'date': transaction_dates[i], 'category': transaction_categories[i]})
            print(f"Transaction records saved to {file_path}.")
    except Exception as e:
        print(f"Error saving transaction records: {str(e)}")
# Function to search sales transactions
def search_sales_transactions(search_string):
    search_string = search_string.lower()
    matching_transactions = []

    for i in range(len(transaction_ids)):
        transaction_id_str = str(transaction_ids[i])
        date = transaction_dates[i].lower()
        category = transaction_categories[i].lower()

        # Check if the search string is found in customer ID, date, category, or value
        if (
            search_string in transaction_id_str
            or search_string in date
            or search_string in category
        ):
            transaction = {
                'transaction_id': transaction_ids[i],
                'customer_id': transaction_customer_ids[i],
                'date': transaction_dates[i],
                'category': transaction_categories[i]
            }
            matching_transactions.append(transaction)

    return matching_transactions



# Function to save all transaction records to a CSV file with user interaction
def save_transactions_to_csv_with_prompt(file_path):
    if os.path.exists(file_path):
        while True:
            user_input = input(f"The file '{file_path}' already exists. Do you want to (C)ancel, (O)verwrite, or (R)ename it? ").strip().lower()
            if user_input == 'c':
                print("Operation canceled.")
                return
            elif user_input == 'o':
                break
            elif user_input == 'r':
                new_file_path = input("Enter a new file path: ").strip()
                file_path = new_file_path
                if not file_path.endswith(".csv"):
                    file_path += ".csv"
                break
            else:
                print("Invalid input. Please enter 'C', 'O', or 'R'.")
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['transaction_id', 'customer_id', 'date', 'category']
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()
            for i in range(len(transaction_ids)):
                csv_writer.writerow({'transaction_id': transaction_ids[i], 'customer_id': transaction_customer_ids[i], 'date': transaction_dates[i], 'category': transaction_categories[i]})
            print(f"Transaction records saved to {file_path}.")
    except Exception as e:
        print(f"Error saving transactions: {str(e)}")





# Function to display transactions for a given customer
def display_customer_transactions(customer_id):
    mask = transaction_customer_ids == customer_id
    customer_transaction_ids = transaction_ids[mask]
    customer_transaction_dates = transaction_dates[mask]
    customer_transaction_categories = transaction_categories[mask]
    customer_transactions = []
    for i in range(len(customer_transaction_ids)):
        transaction = {
            'transaction_id': customer_transaction_ids[i],
            'customer_id': customer_id,
            'date': customer_transaction_dates[i],
            'category': customer_transaction_categories[i]
        }
        customer_transactions.append(transaction)
    return customer_transactions

# Function to delete a transaction by ID
def delete_transaction(transaction_id):
    global transaction_ids, transaction_customer_ids, transaction_dates, transaction_categories
    mask = transaction_ids != transaction_id
    transaction_ids = transaction_ids[mask]
    transaction_customer_ids = transaction_customer_ids[mask]
    transaction_dates = transaction_dates[mask]
    transaction_categories = transaction_categories[mask]


# Define dictionaries to store monthly sales values and transaction numbers
monthly_sales = defaultdict(float)
monthly_transaction_numbers = defaultdict(int)

# Function to calculate monthly sales values and transaction numbers
def calculate_monthly_sales_and_transaction_numbers():
    global transaction_dates, transaction_values, monthly_sales, monthly_transaction_numbers

    # Extract month from the date and initialize monthly sales and transaction numbers
    for date, value in zip(transaction_dates, transaction_values):
        month = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m')
        monthly_sales[month] += value
        monthly_transaction_numbers[month] += 1

# Function to retrieve monthly sales values and transaction numbers
def get_monthly_sales_and_transaction_numbers():
    return monthly_sales, monthly_transaction_numbers

# Function to calculate and display the monthly sales values and transaction numbers
def display_monthly_sales_and_transaction_numbers():
    calculate_monthly_sales_and_transaction_numbers()
    monthly_sales, monthly_transaction_numbers = get_monthly_sales_and_transaction_numbers()

    # Extract data for plotting
    months = list(monthly_sales.keys())
    sales_values = list(monthly_sales.values())
    transaction_numbers = list(monthly_transaction_numbers.values())

    # Create the line graphs
    plt.figure(figsize=(10, 6))
    plt.plot(months, sales_values, label="Monthly Sales Values", marker='o')
    plt.plot(months, transaction_numbers, label="Monthly Transaction Numbers", marker='o')

    # Add titles, labels, and legend
    plt.title("Monthly Sales Values and Transaction Numbers")
    plt.xlabel("Month")
    plt.ylabel("Values / Transaction Numbers")
    plt.legend()

    # Show the plot
    plt.show()