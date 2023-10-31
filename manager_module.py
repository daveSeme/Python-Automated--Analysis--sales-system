import customer_module
import transactions_module
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import csv


from customer_module import add_customer, search_customers
from transactions_module import (
    add_transaction,
    search_sales_transactions,
    delete_transaction,
    calculate_monthly_sales_and_transaction_numbers,
    display_monthly_sales_and_transaction_numbers,
    display_customer_transactions,
)

def add_new_customer(name, postcode="", phone=""):
    return add_customer(name, postcode, phone)

def add_new_transaction(customer_id, date, category):
    return add_transaction(customer_id, date, category)

def search_customers(search_string):
    return customer_module.search_customers(search_string)

def search_sales_transactions(search_string):
    return transactions_module.search_sales_transactions(search_string)

def display_customer_transactions(customer_id):
    customer = customer_module.get_customer_by_id(customer_id)
    if customer is not None:
        customer_transactions = transactions_module.display_customer_transactions(customer_id)
        print(f"Customer Name: {customer['name']}")
        print(f"Customer Postcode: {customer['postcode']}")
        for transaction in customer_transactions:
            print(transaction)
    else:
        print(f"Customer with ID {customer_id} not found.")

def load_customers_from_csv(file_path):
    customer_module.load_customers_from_csv(file_path)

def save_customers_to_csv_with_prompt(file_path):
    customer_module.save_customers_to_csv_with_prompt(file_path)

def load_transactions_from_csv(file_path):
    transactions_module.load_transactions_from_csv(file_path)

def save_transactions_to_csv_with_prompt(file_path):
    transactions_module.save_transactions_to_csv_with_prompt(file_path)

def add_customers_to_existing_csv(file_path):
    customer_module.add_customers_to_existing_csv(file_path)

def delete_customer_and_transactions(customer_id, customer_file_path, transactions_file_path):
    customer_module.delete_customer_and_transactions(customer_id, customer_file_path, transactions_file_path)


# Define a dictionary to map month numbers to month names
month_name_mapping = {
    '01': 'January',
    '02': 'February',
    '03': 'March',
    '04': 'April',
    '05': 'May',
    '06': 'June',
    '07': 'July',
    '08': 'August',
    '09': 'September',
    '10': 'October',
    '11': 'November',
    '12': 'December'
}

def display_monthly_sales_and_transaction_numbers():
    transactions_csv_file = input("Enter the path of the transactions CSV file: ")

    # Initialize dictionaries to store monthly statistics
    monthly_sales = defaultdict(float)
    monthly_transaction_numbers = defaultdict(int)

    # Load data from the transactions CSV file
    with open(transactions_csv_file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for column in csv_reader:
            date = column['date_whole']
            month = date.split('-')[1]  # Extract the month (e.g., '01' from '2020-01-03')
            value = float(column['value'])

            # Replace month with month name
            month = month_name_mapping.get(month, month)

            monthly_sales[month] += value
            monthly_transaction_numbers[month] += 1

        # Create the line graphs
        months = list(monthly_sales.keys())
        sales_values = [monthly_sales[month] for month in months]
        transaction_numbers = [monthly_transaction_numbers[month] for month in months]

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



# will display the monthly sales by postcode
from manager_module import month_name_mapping 
# Define a dictionary to map month numbers to month names
month_name_mapping = {
    '01': 'January',
    '02': 'February',
    '03': 'March',
    '04': 'April',
    '05': 'May',
    '06': 'June',
    '07': 'July',
    '08': 'August',
    '09': 'September',
    '10': 'October',
    '11': 'November',
    '12': 'December',
}
    
def display_postcode_monthly_sales_graph(postcode):
    customer_csv_file = input("Enter the path to the customer CSV file: ")
    transactions_csv_file = input("Enter the path to the transactions CSV file: ")

    # Initialize dictionaries to store monthly statistics
    monthly_sales = defaultdict(float)
    monthly_transaction_numbers = defaultdict(int)

    # Load data from the transactions CSV file
    with open(transactions_csv_file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for column in csv_reader:
            date = column['date_whole']
            month = date.split('-')[1]  # Extract the month (e.g., '01' from '2020-01-03')
            value = float(column['value'])

            # Replace month with month name
            month = month_name_mapping.get(month, month)

            monthly_sales[month] += value
            monthly_transaction_numbers[month] += 1

    # Filter transactions for customers with the given postcode from the customer CSV file
    matching_customers = []
    with open(customer_csv_file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row['postcode'] == postcode:
                matching_customers.append(row)

    postcode_monthly_sales = defaultdict(float)
    postcode_monthly_transactions = defaultdict(int)

    for customer in matching_customers:
        customer_id = customer["customer_id"]

        # Filter transactions for the current customer
        with open(transactions_csv_file, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for column in csv_reader:
                if column['customer_id'] == customer_id:
                    date = column['date_whole']
                    month = date.split('-')[1]  # Extract the month (e.g., '01' from '2020-01-03')
                    value = float(column['value'])

                    # Replace month with month name
                    month = month_name_mapping.get(month, month)

                    postcode_monthly_sales[month] += value
                    postcode_monthly_transactions[month] += 1

    # Create the line graphs
    months = list(monthly_sales.keys())
    sales_values = [monthly_sales[month] for month in months]
    transaction_numbers = [monthly_transaction_numbers[month] for month in months]

    postcode_sales = [postcode_monthly_sales[month] for month in months]
    postcode_transactions = [postcode_monthly_transactions[month] for month in months]

    plt.figure(figsize=(10, 6))
    plt.plot(months, sales_values, label="Monthly Sales Values (All Customers)", marker='o')
    plt.plot(months, transaction_numbers, label="Monthly Transaction Numbers (All Customers)", marker='o')
    plt.plot(months, postcode_sales, label=f"Monthly Sales Values (Postcode: {postcode})", marker='o')
    plt.plot(months, postcode_transactions, label=f"Monthly Transaction Numbers (Postcode: {postcode})", marker='o')

    # Add titles, labels, and legend
    plt.title(f"Monthly Sales Values and Transaction Numbers for Customers in Postcode: {postcode}")
    plt.xlabel("Month")
    plt.ylabel("Values / Transaction Numbers")
    plt.legend()

    # Show the plot
    plt.show()




from manager_module import month_name_mapping 
    
# Define a dictionary to map month numbers to month names
month_name_mapping = {
    '01': 'January',
    '02': 'February',
    '03': 'March',
    '04': 'April',
    '05': 'May',
    '06': 'June',
    '07': 'July',
    '08': 'August',
    '09': 'September',
    '10': 'October',
    '11': 'November',
    '12': 'December',
}



def display_customer_monthly_sales_graph():
    customer_id = input("Enter the customer ID to filter: ")

    # Prompt the user to enter the path of the transactions CSV file
    transactions_csv_file = input("Enter the path of the transactions CSV file: ")

    # Initialize dictionaries to store monthly statistics
    monthly_sales = defaultdict(float)
    monthly_transaction_numbers = defaultdict(int)

    # Load data from the transactions CSV file
    with open(transactions_csv_file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for column in csv_reader:
            if column['customer_id'] == customer_id:
                date = column['date_whole']
                month = date.split('-')[1]  # Extract the month (e.g., '01' from '2020-01-03')
                value = float(column['value'])

                # Replace month with month name using the mapping
                month = month_name_mapping.get(month, month)

                monthly_sales[month] += value
                monthly_transaction_numbers[month] += 1

        # Create the line graphs
        months = list(monthly_sales.keys())
        sales_values = [monthly_sales[month] for month in months]
        transaction_numbers = [monthly_transaction_numbers[month] for month in months]

        plt.figure(figsize=(10, 6))
        plt.plot(months, sales_values, label="Monthly Sales Values", marker='o')
        plt.plot(months, transaction_numbers, label="Monthly Transaction Numbers", marker='o')

        # Add titles, labels, and legend
        plt.title(f"Monthly Sales Values and Transaction Numbers for Customer ID {customer_id}")
        plt.xlabel("Month")
        plt.ylabel("Values / Transaction Numbers")
        plt.legend()

        # Show the plot
        plt.show()