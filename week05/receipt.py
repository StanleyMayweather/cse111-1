"""
File: receipt.py
Author: Stanley Adeyemi Eberendu
Description: Reads a product catalog and a customer request file to 
print a formatted receipt including subtotal, tax, and total.

Enhancement: Prints a 'return by' date that is 9PM 30 days 
in the future at the bottom of the receipt.
"""

import csv
from datetime import datetime, timedelta

def read_dictionary(filename, key_column_index):
    """Read the contents of a CSV file into a compound
    dictionary and return the dictionary.
    
    Parameters:
        filename: the name of the CSV file to read.
        key_column_index: the index of the column to use as keys.
    Return: a compound dictionary.
    """
    compound_dict = {}
    
    with open(filename, "rt") as csv_file:
        reader = csv.reader(csv_file)
        # Skip the header row
        next(reader)
        
        for row_list in reader:
            if len(row_list) != 0:
                key = row_list[key_column_index]
                compound_dict[key] = row_list
                
    return compound_dict

def main():
    # Index constants for products.csv
    PROD_NAME_INDEX = 1
    PROD_PRICE_INDEX = 2
    
    # Index constants for request.csv
    REQ_ID_INDEX = 0
    REQ_QTY_INDEX = 1

    # Store Constants
    STORE_NAME = "Inkom Emporium"
    TAX_RATE = 0.06

    try:
        # 1. Read the product catalog into a dictionary
        products_dict = read_dictionary("products.csv", 0)

        print(STORE_NAME)
        print()

        # 2. Process the request file
        subtotal = 0
        total_items = 0

        with open("request.csv", "rt") as request_file:
            reader = csv.reader(request_file)
            next(reader) # Skip header

            for row in reader:
                product_id = row[REQ_ID_INDEX]
                quantity = int(row[REQ_QTY_INDEX])

                # This line will raise a KeyError if product_id is not found
                product_data = products_dict[product_id]
                
                name = product_data[PROD_NAME_INDEX]
                price = float(product_data[PROD_PRICE_INDEX])

                print(f"{name}: {quantity} @ {price}")

                # Update running totals
                total_items += quantity
                subtotal += (price * quantity)

        # 3. Final Calculations
        sales_tax = subtotal * TAX_RATE
        total_due = subtotal + sales_tax

        # 4. Print Totals
        print()
        print(f"Number of Items: {total_items}")
        print(f"Subtotal: {subtotal:.2f}")
        print(f"Sales Tax: {sales_tax:.2f}")
        print(f"Total: {total_due:.2f}")

        # 5. Footer and Timestamp
        print()
        print(f"Thank you for shopping at the {STORE_NAME}.")
        
        # Current date and time
        now = datetime.now()
        # Formatting example: Wed Nov 04 05:10:30 2020
        print(f"{now:%a %b %d %H:%M:%S %Y}")

        # Enhancement: Return by date (30 days in future at 9:00 PM)
        future_date = now + timedelta(days=30)
        # Construct the return string with the date and hardcoded 9:00 PM
        print(f"Return by: {future_date:%b %d, %Y} at 9:00 PM")

    except FileNotFoundError as file_err:
        print(f"Error: missing file\n{file_err}")
    except PermissionError as perm_err:
        print(f"Error: cannot read file\n{perm_err}")
    except KeyError as key_err:
        print(f"Error: unknown product ID in the request.csv file\n{key_err}")

if __name__ == "__main__":
    main()