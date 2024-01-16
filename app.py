import csv
import os
from datetime import datetime

from db import init_db, Session
from db_utils import create_brand, read_brand_by_id, read_brand_by_name, delete_brand, update_brand, read_all_brands
from db_utils import create_product, read_product, read_all_products, delete_product, update_product, read_product_by_name
from db_utils import find_brand_with_most_products, read_all_products_sorted_one_result
from models import Product, Brands



def main_menu():
    while True:  # Keep them in the main_menu loop until they are ready to exit
        valid_menu_options = ["v", "n", "a", "b", "e"]
        menu_text = """
        \nPlease make a choice:
        V - View Product
        N - New Product
        A - Analyze Products
        B - Backup Data to CSV
        E - Exit
        \n"""
        valid, choice, message = validate_menu_choice(valid_menu_options, menu_text)
        if not valid:
            print(message)
            continue
        else:
            # print(message)
            # print(choice)
            if choice.lower() == "e":  # User requested to exit the application
                break
            elif choice.lower() == "v":
                menu_option_v()
            elif choice.lower() == "n":
                menu_option_n()
            elif choice.lower() == "a":
                menu_option_a()
            elif choice.lower() == "b":
                menu_option_b()


def menu_option_v():
    while True:
        print("*** Submenu: View Product ***")
        user_entered_id = validate_user_input('integer', "what is the product_id for the product you want to view?: ")
        product = read_product(user_entered_id)
        if not product:
            print("Sorry. No results for the product_id")
        else:
            print(product)


        # Continue or exit submenu
        while True:
            menu_text = "\nWould you like to continue? \nR for Return or C for Continue: "
            valid, choice, message = validate_menu_choice(["r", "c"], menu_text)
            if valid and choice.lower() == 'r':
                return
            elif valid and choice.lower() == 'c':
                break
            else:
                print(message)



def menu_option_n():
    while True:
        print("*** Submenu: New Product ***")
        user_entered_brand_name = validate_user_input('string', "what is the brand_name: ")
        brand = read_brand_by_name(user_entered_brand_name)
        if not brand:
            print("Brand Not Found. Creating New Brand.")
            status, message = create_brand(user_entered_brand_name)
            if status:
                print(message)
                brand = read_brand_by_name(user_entered_brand_name)
                if not brand:
                    print("Error creating brand")
            else:
                print(message)

        product_name = validate_user_input('string', "product name: ")
        product_quantity = validate_user_input('integer', "product quantity: ")
        product_price = validate_user_input('float', "product price: ")
        product_price = convert_price_to_cents(product_price)
        brand_id = brand.brand_id

        created, message = create_product(product_name=product_name,
                                          product_quantity=product_quantity,
                                          product_price=product_price,
                                          brand_id=brand_id)
        print(message)

        # Continue or exit submenu
        while True:
            menu_text = "\nWould you like to continue? \nR for Return or C for Continue: "
            valid, choice, message = validate_menu_choice(["r", "c"], menu_text)
            if valid and choice.lower() == 'r':
                return
            elif valid and choice.lower() == 'c':
                break
            else:
                print(message)



def menu_option_a():
    while True:
        print("*** Submenu: Analyze Database ***")

        print("\nHere are the analysis results")
        # What is the most expensive item
        most_expensive = read_all_products_sorted_one_result('max')
        print("\nMost Expensive Item:")
        print(most_expensive)

        # What is the least expensive item
        least_expensive = read_all_products_sorted_one_result('min')
        print("\nLeast Expensive Item:")
        print(least_expensive)

        # Which brand has the most products
        brand_id, quantity = find_brand_with_most_products()
        brand = read_brand_by_id(brand_id)
        print("\nBrand with the most products:")
        print(f"brand name: {brand.brand_name}")
        print(f"quantity: {quantity}")

        # Continue or exit submenu
        while True:
            menu_text = "\nWould you like to continue? \nR for Return or C for Continue: "
            valid, choice, message = validate_menu_choice(["r", "c"], menu_text)
            if valid and choice.lower() == 'r':
                return
            elif valid and choice.lower() == 'c':
                break
            else:
                print(message)



def menu_option_b():
    while True:
        print("Submenu: Backup the Database")

        # Directory for backups
        backup_dir = 'backups'

        # Check if the directory exists, and create it if it doesn't
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir, exist_ok=True)


        # Backup Products
        print("Beginning Backup of Products")
        try:
            all_products = read_all_products()
            with open(os.path.join(backup_dir, 'products_backup.csv'), 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['product_id',
                                 'product_name',
                                 'product_quantity',
                                 'product_price',
                                 'date_updated',
                                 'brand_id'])  # headers row for the csv
                for product in all_products:
                    writer.writerow(
                        [product.product_id,
                         product.product_name,
                         product.product_quantity,
                         product.product_price,
                         product.date_updated,
                         product.brand_id])
            print("Backup Successful")
        except:
            print("Error Backing up Products")


        # Backup Brands
        print("Beginning Backup of Brands")
        try:
            all_brands = read_all_brands()
            with open(os.path.join(backup_dir, 'brands_backup.csv'), 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['brand_id', 'brand_name'])  # headers
                for brand in all_brands:
                    writer.writerow([brand.brand_id, brand.brand_name])
            print("Backup Successful")
        except:
            print("Error Backing up Brands")


        # Continue or exit submenu
        while True:
            menu_text = "\nWould you like to continue? \nR for Return or C for Continue: "
            valid, choice, message = validate_menu_choice(["r", "c"], menu_text)
            if valid and choice.lower() == 'r':
                return
            elif valid and choice.lower() == 'c':
                break
            else:
                print(message)



def convert_price_to_cents(price_float):
    return int(price_float * 100)


def validate_menu_choice(valid_menu_options, menu_text):
    choice = input(menu_text)
    if choice.lower() in valid_menu_options:
        valid = True
        message = "valid input selected"
    else:
        valid = False
        message = f"User Error: invalid input. Choice not in list: {valid_menu_options}"
    return valid, choice, message


def validate_user_input(valid_type, prompt_text):
    while True:
        choice = input(prompt_text)
        if choice == '':  # Check if the input is blank
            message = "Invalid Input. Blank spaces are not allowed"
            print(message)

        if valid_type == "string":
            for char in choice:
                if char.isdigit():  # check if the string contains digits
                    print("Invalid Input. String must not contain numbers")
                else:
                    return choice
        elif valid_type == "integer":
            try:
                choice = int(choice)  # Check if it can be converted to an integer
                if choice >= 0:
                    return choice
                else:
                    print("Invalid Input. Integer must not be negative")
            except:
                message = "Invalid Input. Input is not an Integer"
                print(message)
        elif valid_type == "float":
            try:
                choice = float(choice)   # Check if it can be converted to a float
                return choice
            except:
                message = "Invalid Input. Input is not an valid Float format (0.05, 4.53, etc.)"
                print(message)





def load_csv_data_into_db_brands():

    seed_dir = 'seed_files'
    brands_file = os.path.join(seed_dir, 'brands.csv')

    session = Session()

    # Load Brands
    if os.path.exists(brands_file):
        with open(brands_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                brand = Brands(brand_name=row['brand_name'])
                session.add(brand)
    else:
        print(f"Brands file not found: {brands_file}")

    # Commit the session to save changes
    try:
        session.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()



def load_csv_data_into_db_products():

    seed_dir = 'seed_files'
    products_file = os.path.join(seed_dir, 'inventory.csv')

    session = Session()

    # Load Products
    if os.path.exists(products_file):
        with open(products_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:

                product_name = row['product_name']
                # Check if product name already exists in db
                try:
                    product = read_product_by_name(product_name)
                except:
                    product = None

                if not product:
                    brand_name = row['brand_name']
                    brand = read_brand_by_name(brand_name)
                    brand_id = brand.brand_id

                    price_field = row['product_price']
                    product_price = int(float(price_field[1:len(price_field)]) * 100)

                    product_quantity = int(row['product_quantity'])


                    date_updated = datetime.strptime(row["date_updated"], '%m/%d/%Y').date()

                    product = Product(
                        product_name=product_name,
                        product_price=product_price,
                        product_quantity=product_quantity,
                        date_updated=date_updated,
                        brand_id=brand_id
                    )
                    session.add(product)
                else:  # Else meaning that the query returned a product with a matching name
                    print(f"Product already exists for product: {product.product_name}  | date_updated: {product.date_updated}")
                    old_date_updated = product.date_updated
                    new_date_updated = datetime.strptime(row["date_updated"], '%m/%d/%Y').date()

                    if new_date_updated > old_date_updated:  # Check if the updated date is newer
                        print(f"The data for this item is more recently updated ({new_date_updated}) - updating item information")
                        brand_name = row['brand_name']
                        brand = read_brand_by_name(brand_name)
                        brand_id = brand.brand_id
                        price_field = row['product_price']
                        product_price = int(float(price_field[1:len(price_field)]) * 100)
                        product_quantity = int(row['product_quantity'])

                        # Modify the object
                        product.product_name = product_name
                        product.product_price = product_price
                        product.product_quantity = product_quantity
                        product.brand_id = brand_id
                        product.date_updated = new_date_updated


    else:
        print(f"Products file not found: {products_file}")

    # Commit the session to save changes
    try:
        session.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()


def greeting():
    print("Welcome to the Store Inventory App!")



def goodbye():
    print("Thank You. Goodbye!")



if __name__ == '__main__':
    init_db()
    load_csv_data_into_db_brands()
    load_csv_data_into_db_products()
    greeting()
    main_menu()
    goodbye()


