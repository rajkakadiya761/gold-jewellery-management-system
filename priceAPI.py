# def make_gapi_request():
#     # api_key = "goldapi-4fdjs3fsm6es0363-io"
#     api_key = "goldapi-jti2sm6dzkgyp-io"
#     metals = ["XAU", "XAG", "XPT"]  # Gold, Silver, Platinum
#     curr = "INR"
#     prices = {}

#     for metal in metals:
#         url = f"https://www.goldapi.io/api/{metal}/{curr}"
        
#         headers = {
#             "x-access-token": api_key,
#             "Content-Type": "application/json"
#         }
        
#         try:
#             response = requests.get(url, headers=headers)
#             response.raise_for_status()
#             result = response.json()
            
#             # Get the price for 1 gram (if available) or price field in INR
#             price_per_gram = result.get('price_gram_24k') if metal == "XAU" else result.get('price')
#             prices[metal] = round(price_per_gram, 2) if price_per_gram else "Data Unavailable"

#         except requests.exceptions.RequestException as e:
#             print(f"Error fetching {metal} price:", str(e))
#             prices[metal] = "Error"

#     return prices

from flask import jsonify,request
from flask import Blueprint, current_app
import requests
from models import db, Products, ProductPricing, ProductMaterial, Material

pricing_bp = Blueprint("pricing", __name__)  # Create a Blueprint

def make_gapi_request():
    """Fetches live metal prices per gram in INR with proper currency and unit conversions."""
    api_key = "goldapi-7dilism6z5h88g-io"
    metals = {"XAU": "gold", "XAG": "silver", "XPT": "platinum"}
    
    usd_to_inr = 88.00 
    ounce_to_gram = 31.1035  # 1 troy ounce = 31.1035 grams

    prices = {"XAU": "N/A", "XAG": "N/A", "XPT": "N/A"}  # Default values

    for metal, name in metals.items():
        url = f"https://www.goldapi.io/api/{metal}/USD"  # Fetch in USD (not INR)
        headers = {"x-access-token": api_key, "Content-Type": "application/json"}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            result = response.json()

            if metal == "XAU":  
                # Gold price is usually given per gram (but in USD)
                price_per_gram_usd = result.get("price_gram_24k")
                if price_per_gram_usd:
                    price_per_gram = price_per_gram_usd * usd_to_inr  # Convert to INR
                else:
                    price_per_gram = None

            else:  # Silver (XAG) and Platinum (XPT)
                price_per_ounce_usd = result.get("price")  # Likely per ounce in USD
                if price_per_ounce_usd:
                    price_per_gram = (price_per_ounce_usd / ounce_to_gram) * usd_to_inr  # Convert to INR per gram
                else:
                    price_per_gram = None

            if price_per_gram is not None:
                prices[metal] = round(price_per_gram, 2)
            else:
                print(f"Warning: No valid price found for {name}.")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {name} price: {e}")

    return prices  


print(make_gapi_request())

def update_product_pricing():
    """Updates product pricing based on the latest metal prices."""
    with current_app.app_context():  # Ensure Flask app context
        prices = make_gapi_request()  # Fetch latest metal prices

        # Fetch all products that have a linked material
        products = db.session.query(Products).join(ProductMaterial).join(Material).all()

        for product in products:
            # Get the first linked material (assuming one material per product)
            product_material = product.product_materials[0] if product.product_materials else None
            
            if not product_material:
                print(f"Skipping {product.name}: No material linked.")
                continue

            material_name = product_material.material.material_name.lower()
            metal_code = None

            # Map DB material name to API metal code
            if material_name == "gold":
                metal_code = "XAU"
            elif material_name == "silver":
                metal_code = "XAG"
            elif material_name == "platinum":
                metal_code = "XPT"

            if not metal_code or metal_code not in prices:
                print(f"Skipping {product.name}: No valid price for {material_name}.")
                continue

            # Calculate final price
            material_price_per_gram = prices[metal_code]
            final_price = round(product.product_weight * material_price_per_gram, 2)

            # Check if an entry exists in ProductPricing
            pricing_entry = ProductPricing.query.filter_by(product_id=product.product_id).first()

            if pricing_entry:
                pricing_entry.price = final_price  # Update existing price
            else:
                new_pricing = ProductPricing(product_id=product.product_id, price=final_price, quantity=10)
                db.session.add(new_pricing)  # Insert new entry

            print(f"Updated {product.name}: ₹{final_price}")

        db.session.commit()  # Commit changes to database
        print("Product pricing updated successfully!")

@pricing_bp.route('/add_productPrice', methods=['POST'])
def add_product():
    """Adds a new product and automatically updates pricing."""
    try:
        data = request.get_json()
        name = data['name']
        description = data['description']
        product_weight = data['product_weight']
        sizes = data['sizes']
        category = data['category']
        material_name = data['material']  # Material name from request
        photo1 = data['photo1']
        photo2 = data['photo2']

        # Find or create material
        material = Material.query.filter_by(material_name=material_name.lower()).first()
        if not material:
            return jsonify({"error": "Invalid material type"}), 400

        # Add product entry
        new_product = Products(
            name=name, description=description,
            product_weight=product_weight, sizes=sizes,
            category=category, photo1=photo1, photo2=photo2
        )
        db.session.add(new_product)
        db.session.flush()  # Get the new product ID

        # Link product with material
        new_product_material = ProductMaterial(
            product_id=new_product.product_id, material_id=material.material_id
        )
        db.session.add(new_product_material)
        db.session.commit()

        # Update HomeProducts table
        update_product_pricing()

        return jsonify({"message": "Product added successfully!", "product_id": new_product.product_id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

