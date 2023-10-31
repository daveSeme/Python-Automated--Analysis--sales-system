import random
import csv
import numpy as np
from collections import defaultdict
import os

# Initialize NumPy arrays for customers
customer_ids = np.array([], dtype=int)
customer_names = np.array([], dtype=str)
customer_postcodes = np.array([], dtype=str)
customer_phones = np.array([], dtype=str)

# A function to generate a random customer ID
def generate_customer_id():
    return random.randint(1, 999999)

# Function to add a new customer
def add_customer(name, postcode="", phone=""):
    global customer_ids, customer_names, customer_postcodes, customer_phones  

    customer_id = generate_customer_id()
    customer_ids = np.append(customer_ids, customer_id)
    customer_names = np.append(customer_names, name)
    customer_postcodes = np.append(customer_postcodes, postcode)
    customer_phones = np.append(customer_phones, phone)

    customer = {
        'customer_id': customer_id,
        'name': name,
        'postcode': postcode,
        'phone': phone
    }
    return customer

def load_customers_from_csv(file_path):
    global customer_ids, customer_names, customer_postcodes, customer_phones

    try:
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if 'customer_id' in row and 'name' in row:
                    customer_id = int(row['customer_id'])
                    name = row['name']
                    postcode = row.get('postcode', "")  
                    phone = row.get('phone', "")  

                    if customer_id not in customer_ids:
                        customer_ids = np.append(customer_ids, customer_id)
                        customer_names = np.append(customer_names, name)
                        customer_postcodes = np.append(customer_postcodes, postcode)
                        customer_phones = np.append(customer_phones, phone)
                    else:
                        print(f"Skipping duplicate customer ID: {customer_id}")
                else:
                    print("Skipping row with missing 'customer_id' or 'name'")

        print(f"Customer records loaded from {file_path}.")
    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print(f"Error: {str(e)}")
        
# Function to save customer records to a CSV file with user interaction
def save_customers_to_csv_with_prompt(file_path):
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
            fieldnames = ['customer_id', 'name', 'postcode', 'phone']
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()
            for i in range(len(customer_ids)):
                csv_writer.writerow({'customer_id': customer_ids[i], 'name': customer_names[i], 'postcode': customer_postcodes[i], 'phone': customer_phones[i]})
            print(f"Customer records saved to {file_path}.")
    except Exception as e:
        print(f"Error saving customer records: {str(e)}")

def add_customers_to_existing_csv(file_path):
    if not os.path.exists(file_path):
        print(f"The file '{file_path}' does not exist.")
        return

    try:
        with open(file_path, 'a', newline='') as csv_file:
            fieldnames = ['customer_id', 'name', 'postcode', 'phone']
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Check if the file is empty, and write the header only if it's empty
            if os.path.getsize(file_path) == 0:
                csv_writer.writeheader()

            for i in range(len(customer_ids)):
                csv_writer.writerow({'customer_id': customer_ids[i], 'name': customer_names[i], 'postcode': customer_postcodes[i], 'phone': customer_phones[i]})
            print(f"Customer records added to {file_path}.")
    except Exception as e:
        print(f"Error: {str(e)}")


# Function to search customers by a single search string (case-insensitive and partial match)
def search_customers(search_string):
    search_string = search_string.lower()  # Convert the search string to lowercase
    matching_customers = []

    for i in range(len(customer_ids)):
        # Convert all relevant fields to lowercase for case-insensitive comparison
        customer_id_str = str(customer_ids[i])
        name = customer_names[i].lower()
        postcode = customer_postcodes[i].lower()
        phone = customer_phones[i].lower()

        # Check if the search string is found in customer ID, name, postcode, or phone number
        if (
            search_string in customer_id_str
            or search_string in name
            or search_string in postcode
            or search_string in phone
        ):
            customer = {
                'customer_id': customer_ids[i],
                'name': customer_names[i],
                'postcode': customer_postcodes[i],
                'phone': customer_phones[i]
            }
            matching_customers.append(customer)

    return matching_customers


def delete_customer_and_transactions(customer_id, customer_file_path, transactions_file_path):
    # Load customer data
    try:
        with open(customer_file_path, 'r', newline='') as customer_csv:
            customer_data = list(csv.DictReader(customer_csv))
    except FileNotFoundError:
        print("Customer file not found")
        return

    # Filter out the specified customer
    customer_removed = None
    updated_customer_data = []
    for customer in customer_data:
        if int(customer['customer_id']) == customer_id:
            customer_removed = customer
        else:
            updated_customer_data.append(customer)

    if customer_removed is None:
        print(f"Customer with ID {customer_id} not found in the customer CSV file.")
        return

    # Write the updated customer data back to the customer CSV file
    try:
        with open(customer_file_path, 'w', newline='') as customer_csv:
            fieldnames = ['customer_id', 'name', 'postcode', 'phone']
            csv_writer = csv.DictWriter(customer_csv, fieldnames=fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(updated_customer_data)
        print(f"Customer with ID {customer_id} and their associated transactions have been deleted from the customer CSV file.")
    except Exception as e:
        print(f"Error updating customer CSV file: {str(e)}")

    # Load transaction data
    try:
        with open(transactions_file_path, 'r', newline='') as transactions_csv:
            transactions_data = list(csv.DictReader(transactions_csv))
    except FileNotFoundError:
        print("Transactions file not found")
        return

    # Filter out transactions associated with the deleted customer
    updated_transactions_data = [transaction for transaction in transactions_data if int(transaction['customer_id']) != customer_id]

    # Write the updated transaction data back to the transactions CSV file
    try:
        with open(transactions_file_path, 'w', newline='') as transactions_csv:
            fieldnames = ['transaction_id', 'customer_id', 'date', 'category']
            csv_writer = csv.DictWriter(transactions_csv, fieldnames=fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(updated_transactions_data)
        print(f"Associated transaction records for customer with ID {customer_id} have been deleted from the transactions CSV file.")
    except Exception as e:
        print(f"Error updating transactions CSV file: {str(e)}")
        
        # Function to get a customer by their ID
def get_customer_by_id(customer_id):
    index = np.where(customer_ids == customer_id)
    if index[0].size > 0:
        return {
            "customer_id": customer_ids[index],
            "name": customer_names[index],
            "postcode": customer_postcodes[index],
            "phone": customer_phones[index],
        }
    return None