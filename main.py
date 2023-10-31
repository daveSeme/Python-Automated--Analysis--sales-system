import manager_module
import numpy as np
import matplotlib.pyplot as plt

while True:
    print("\nWestern Wholesales Pty Ltd Menu:")
    print("1. Add a new customer")
    print("2. Add a new transaction")
    print("3. Search customers")
    print("4. Search transactions")
    print("5. Display transactions for a customer")
    print("6. Delete a transaction")
    print("7. Delete a customer and their transactions")
    print("8. Load customer records from CSV")
    print("9. Save customer records to CSV")
    print("10. Load transaction records from CSV")
    print("11. Save transaction records to CSV")
    print("12. Display Monthly Sales Values and Transaction Numbers")
    print("13. Display Monthly Sales Values and Transaction Numbers for a Given Customer")
    print("14. Display Monthly Sales Values and Transaction Numbers for a Given Postcode")
    print("15. Quit")

    choice = input("Enter your choice: ")

    if choice == '1':
        name = input("Enter customer name: ")
        postcode = input("Enter customer postcode (optional): ")
        phone = input("Enter customer phone number (optional): ")
        customer = manager_module.add_new_customer(name, postcode, phone)
        print(f"Customer {customer['customer_id']} ({customer['name']}) added successfully.")
        
    elif choice == '2':
        customer_id = int(input("Enter customer ID: "))
        date = input("Enter transaction date: ")
        
        valid_categories = ["food", "alcohol and beverage", "apparel", "furniture", "household appliances", "computer equipment"]
        while True:
            category = input("Enter transaction category: ")
            if category.lower() in valid_categories:
                break
            else:
                print("Invalid category. Please enter a valid category from the list.")

        transaction = manager_module.add_new_transaction(customer_id, date, category)  
        print(f"Transaction {transaction['transaction_id']} added for customer {customer_id}.")

    elif choice == '3':
        search_string = input("Enter a search string: ")
        matching_customers = manager_module.search_customers(search_string)
        if matching_customers:
            for customer in matching_customers:
                print(f"Customer ID: {customer['customer_id']}, Name: {customer['name']}, Postcode: {customer['postcode']}, Phone: {customer['phone']}")
        else:
            print("No matching customers found.") 
 
    elif choice == '4':
        search_string = input("Enter a search string: ")
        matching_transactions = manager_module.search_sales_transactions(search_string)
        if matching_transactions:
            for transaction in matching_transactions:
                print(f"Transaction ID: {transaction['transaction_id']}, Customer ID: {transaction['customer_id']}, Date: {transaction['date']}, Category: {transaction['category']}")
        else:
            print("No matching transactions found.")
    elif choice == '5':
        customer_id = int(input("Enter customer ID: "))
        matching_transactions = manager_module.display_customer_transactions(customer_id)
        if matching_transactions:
            for transaction in matching_transactions:
                print(f"Transaction ID: {transaction['transaction_id']}, Date: {transaction['date']}, Category: {transaction['category']}")
        else:
            print("No transactions found for this customer.")
    elif choice == '6':
        transaction_id = int(input("Enter transaction ID to delete: "))
        manager_module.delete_transaction(transaction_id)
    elif choice == '7':
        customer_id = int(input("Enter customer ID to delete, along with their transactions: "))
        customer_file_path = input("Enter the path of the customer CSV file: ")
        transactions_file_path = input("Enter the path of the transactions CSV file: ")
        manager_module.delete_customer_and_transactions(customer_id, customer_file_path, transactions_file_path)
    elif choice == '8':
        customer_file_path = input("Enter the path of the customer CSV file: ")
        manager_module.load_customers_from_csv(customer_file_path)
    elif choice == '9':
        file_path = input("Enter the path of the CSV file to save customers: ")
        manager_module.save_customers_to_csv_with_prompt(file_path)
    elif choice == '10':
        transactions_file_path = input("Enter the path of the transactions CSV file: ")
        manager_module.load_transactions_from_csv(transactions_file_path)
    elif choice == '11':
        file_path = input("Enter the path of the CSV file to save transactions: ")
        manager_module.save_transactions_to_csv_with_prompt(file_path)
    elif choice == '12':
        manager_module.display_monthly_sales_and_transaction_numbers()
    elif choice == '13':
        customer_id = input("Enter the customer ID to filter: ")
        transactions_file_path = input("Enter the path of the transactions CSV file: ")
        manager_module.display_customer_monthly_sales_graph()
    elif choice == '14':
        postcode = input("Enter postcode: ")
        manager_module.display_postcode_monthly_sales_graph(postcode)
    elif choice == '15':
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please select a valid option.")