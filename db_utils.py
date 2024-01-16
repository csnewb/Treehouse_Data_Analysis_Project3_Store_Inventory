from sqlalchemy import func
from models import Product, Brands
from db import Session

################## Brands #################
def read_all_brands():
    session = Session()
    try:
        brands = session.query(Brands).all()
        return brands
    except Exception as e:
        print(f"Error reading all brands: {e}")
        return []
    finally:
        session.close()

def create_brand(brand_name):
    session = Session()
    try:
        new_brand = Brands(brand_name=brand_name)
        session.add(new_brand)
        session.commit()
        return True, "Brand added successfully"
    except Exception as e:
        session.rollback()
        return False, f"Error adding brand: {e}"
    finally:
        session.close()

def read_brand_by_id(brand_id):
    session = Session()
    try:
        brand = session.query(Brands).filter(Brands.brand_id == brand_id).first()
        return brand
    except Exception as e:
        print(f"Error reading brand {brand_id}: {e}")
        return None
    finally:
        session.close()

def read_brand_by_name(brand_name):
    session = Session()
    try:
        brand = session.query(Brands).filter(Brands.brand_name == brand_name).first()
        return brand
    except Exception as e:
        print(f"Error reading brand {brand_name}: {e}")
        return None
    finally:
        session.close()

def update_brand(brand_id, new_brand_name):
    session = Session()
    try:
        brand = session.query(Brands).filter(Brands.brand_id == brand_id).first()
        if brand:
            brand.brand_name = new_brand_name
            session.commit()
            return True, "Brand updated successfully"
        else:
            return False, "Brand not found"
    except Exception as e:
        session.rollback()
        return False, f"Error updating brand: {e}"
    finally:
        session.close()

def delete_brand(brand_id):
    session = Session()
    try:
        brand = session.query(Brands).filter(Brands.brand_id == brand_id).first()
        if brand:
            session.delete(brand)
            session.commit()
            return True, "Brand deleted successfully"
        else:
            return False, "Brand not found"
    except Exception as e:
        session.rollback()
        return False, f"Error deleting brand: {e}"
    finally:
        session.close()


################ Products ###################
def read_all_products():
    session = Session()
    try:
        products = session.query(Product).all()
        return products
    except Exception as e:
        # Handle or log the exception if needed
        return []
    finally:
        session.close()

def create_product(product_name, product_quantity, product_price, brand_id):
    session = Session()
    try:
        new_product = Product(product_name=product_name,
                              product_quantity=product_quantity,
                              product_price=product_price,
                              brand_id=brand_id)
        session.add(new_product)
        session.commit()
        return True, "Product added successfully"
    except Exception as e:
        session.rollback()
        return False, f"Error adding product: {e}"
    finally:
        session.close()

def read_product(product_id):
    session = Session()
    try:
        product = session.query(Product).filter(Product.product_id == product_id).first()
        return product
    except Exception as e:
        print(f"Error reading product {product_id}: {e}")
        return None
    finally:
        session.close()


def read_product_by_name(product_name):
    session = Session()
    try:
        product = session.query(Product).filter(Product.product_name == product_name).first()
        return product
    except Exception as e:
        print(f"Error reading product {product_name}: {e}")
        return None
    finally:
        session.close()


def update_product(product_id, new_name, new_quantity, new_price):
    session = Session()
    try:
        product = session.query(Product).filter(Product.product_id == product_id).first()
        if product:
            product.product_name = new_name
            product.product_quantity = new_quantity
            product.product_price = new_price
            session.commit()
            return True, "Product updated successfully"
        else:
            return False, "Product not found"
    except Exception as e:
        session.rollback()
        return False, f"Error updating product: {e}"
    finally:
        session.close()

def delete_product(product_id):
    session = Session()
    try:
        product = session.query(Product).filter(Product.product_id == product_id).first()
        if product:
            session.delete(product)
            session.commit()
            return True, "Product deleted successfully"
        else:
            return False, "Product not found"
    except Exception as e:
        session.rollback()
        return False, f"Error deleting product: {e}"
    finally:
        session.close()


def find_brand_with_most_products():
    session = Session()
    try:

        result = session.query(
            Product.brand_id,
            func.count(Product.product_id).label('product_count')  # create a new column to store the count
        ).group_by(
            Product.brand_id  # Segement the data by the brand_id
        ).order_by(
            func.count(Product.product_id).desc()  # To sort it highest to lowest so we can grab the first result
        ).limit(1).first()

        return result  # Returns a tuple (brand_id, product_count)
    except Exception as e:
        print(f"Error occurred: {e}")
        return None
    finally:
        session.close()


def read_all_products_sorted_one_result(sort):
    session = Session()
    try:
        if sort == "min":
            products = session.query(Product).order_by(Product.product_price.asc()).first()
        else:
            products = session.query(Product).order_by(Product.product_price.desc()).first()
        return products
    except Exception as e:
        print(f"Error occurred: {e}")
        return []
    finally:
        session.close()

