from flask import Blueprint, render_template, request, flash, redirect, session, url_for
from models import ProductPricing, db, Products, Material, ProductMaterial
from priceAPI import make_gapi_request

# Create Blueprint for product management
manage_products_bp = Blueprint('manage_products', __name__)

@manage_products_bp.route('/manage-products', methods=['POST'])
def manage_products():
    products = Products.query.all()  # Get all products
    materials = Material.query.all()  # Get all materials
    product_materials = ProductMaterial.query.all()  # Get all product-material relationships
    pricing = {p.product_id: {'price': p.price, 'quantity': p.quantity} for p in ProductPricing.query.all()}

    # Map product IDs to their materials
    product_material_map = {}
    for pm in product_materials:
        material_name = next((m.material_name for m in materials if m.material_id == pm.material_id), None)
        if pm.product_id in product_material_map:
            product_material_map[pm.product_id].append(material_name)
        else:
            product_material_map[pm.product_id] = [material_name]
            
    for product in products:
        product.material_ids = [
            pm.material_id for pm in product_materials if pm.product_id == product.product_id
        ]
        
        product.price = pricing.get(product.product_id, {}).get('price', 'N/A')
        product.quantity = pricing.get(product.product_id, {}).get('quantity', 'N/A')

    return render_template(
        'manageProducts.html',
        products=products,
        product_material_map=product_material_map,
        materials=materials,
        pricing=pricing
    )
    
@manage_products_bp.route('/add-product', methods=['POST'])
def add_product():
    try:
        name = request.form['name']
        description = request.form['description']
        product_weight = request.form['product_weight']
        category = request.form['category']
        gender = request.form['Gender']  
        occasion = request.form.get('Occasion', 'Minimal')
        photo1 = request.form['photo1']
        photo2 = request.form['photo2']
        photo3 = request.form.get('photo3', '')
        photo4 = request.form.get('photo4', '')
        material_id = request.form['material_id']
        sizes = request.form.getlist('sizes') 
        quantity = request.form['quantity']
        if not sizes:
            sizes = ["medium"]

        size_str = ",".join(sizes)
        
        if not all([name, description, product_weight, size_str, category, photo1, photo2, material_id, quantity]):
            flash("All fields are required.", "danger")
            return redirect(url_for('manage_products.manage_products'))
        
        existing_product = Products.query.filter_by(
            name=name,
            description=description,
            product_weight=product_weight,
            sizes=size_str,
            category=category,
            Gender=gender,
            Occasion=occasion,
            photo1=photo1,
            photo2=photo2,
            photo3=photo3,
            photo4=photo4,
            # quantity=quantity
        ).first()

        if existing_product:
            addret=manage_products()
            return addret
        
        if float(product_weight) <= 0:  # Ensures weight is greater than 0
           flash("Weight must be greater than zero!")
           addret=manage_products()
           return addret

        # Create and add the product
        new_product = Products(
            name=name,
            description=description,
            product_weight=product_weight,
            sizes=size_str,
            category=category,
            Gender=gender,
            Occasion=occasion,
            photo1=photo1,
            photo2=photo2,
            photo3=photo3,
            photo4=photo4
        )
        db.session.add(new_product)
        db.session.commit()  # Commit to generate product_id

        # Refresh the session to ensure product_id is updated
        db.session.refresh(new_product)


        # Now add the material relationship (product_id -> material_id)
        product_material = ProductMaterial(product_id=new_product.product_id, material_id=material_id)
        db.session.add(product_material)
        db.session.commit()  # Commit the relationship


        price = calculate_product_price(product_weight, material_id)
        if price is not None:
            # Insert product price into ProductPricing table
            pricing_entry = ProductPricing(product_id=new_product.product_id, price=price, quantity=quantity)
            db.session.add(pricing_entry)
            db.session.commit()
            flash(f"Product added successfully! Calculated price: ₹{price}", "success")
            addret=manage_products()
            return addret
        else:
            flash("Failed to calculate product price.", "danger")
            addret=manage_products()
            return addret

    except Exception as e:
        db.session.rollback()
        flash(f"Error adding product: {str(e)}", "danger")
    addret=manage_products()
    return addret

@manage_products_bp.route('/update-product/<int:product_id>', methods=['POST'])
def update_product(product_id):
    try:
        product = Products.query.get(product_id)
        if not product:
            flash("Product not found.", "danger")
            return manage_products()

        # Fetch material-product relationship first
        product_material = ProductMaterial.query.filter_by(product_id=product_id).first()

        # Fetch updated values
        product.name = request.form['name']
        product.description = request.form['description']
        product.product_weight = request.form['product_weight']
        product.category = request.form['category']
        product.Gender = request.form.get('Gender', product.Gender)  
        product.Occasion = request.form.get('Occasion', product.Occasion)  
        product.photo1 = request.form['photo1']
        product.photo2 = request.form['photo2']
        product.photo3 = request.form.get('photo3', product.photo3)  # Avoid KeyError
        product.photo4 = request.form.get('photo4', product.photo4)  # Avoid KeyError

        # Fetch sizes
        selected_sizes = request.form.getlist('sizes')
        if not selected_sizes:
            selected_sizes = ["medium"]
        product.sizes = ",".join(selected_sizes)

        # Fetch and validate product weight
        new_weight = request.form.get('product_weight', '').strip()
        if new_weight and new_weight.replace('.', '', 1).isdigit():
            new_weight = float(new_weight)
            if new_weight > 0:
                product.product_weight = new_weight
            else:
                flash("Weight must be greater than zero!", "warning")
        else:
            flash("Invalid weight input.", "danger")
            return manage_products()

        # Fetch material_id
        material_id = request.form.get('material_id')
        if material_id:
            if product_material:
                product_material.material_id = material_id
            else:
                product_material = ProductMaterial(product_id=product_id, material_id=material_id)
                db.session.add(product_material)

        # Fetch and validate quantity
        new_quantity = request.form.get('quantity', '').strip()
        if new_quantity.isdigit():
            new_quantity = int(new_quantity)
            if new_quantity < 0:
                flash("Quantity cannot be negative!", "warning")
                return manage_products()
        else:
            flash("Invalid quantity value!", "danger")
            return manage_products()

        # Update price if weight and material are available
        if new_weight and material_id:
            new_price = calculate_product_price(new_weight, material_id)
            if new_price is None:
                flash("Price calculation failed.", "danger")
                return manage_products()
        else:
            new_price = None

        # Update pricing in ProductPricing table
        pricing_entry = ProductPricing.query.filter_by(product_id=product_id).first()
        if pricing_entry:
            pricing_entry.price = new_price
            pricing_entry.quantity = new_quantity
        else:
            if new_price is not None:  # Avoid inserting null price
                new_pricing = ProductPricing(product_id=product_id, price=new_price, quantity=new_quantity)
                db.session.add(new_pricing)

        # Commit changes
        db.session.commit()
        flash("Product updated successfully!", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Error updating product: {str(e)}", "danger")

    return manage_products()

@manage_products_bp.route('/delete-product/<int:product_id>', methods=['GET'])
def delete_product(product_id):
    try:
        # Delete product-material relationships first
        ProductMaterial.query.filter_by(product_id=product_id).delete()
        ProductPricing.query.filter_by(product_id=product_id).delete()

        # Delete product
        product = Products.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()

        flash("Product deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting product: {str(e)}", "danger")

    # return redirect(url_for('manage_products.manage_products'))
    dltret=manage_products()
    return dltret

def calculate_product_price(product_weight, material_id):
    try:
        # Fetch live prices using the existing make_gapi_request function
        prices = make_gapi_request()

        # Get material name for the given material_id
        material = Material.query.get(material_id)
        if not material:
            print(f"Material with ID {material_id} not found.")
            return None

        # Map material names to API metals
        metal_map = {"gold": "XAU", "silver": "XAG", "platinum": "XPT"}
        metal_key = metal_map.get(material.material_name.lower())

        if metal_key and prices.get(metal_key) != "N/A":
            price_per_gram = prices[metal_key]
            product_price = round(float(product_weight) * price_per_gram, 2)
            print(f"Calculated product price for {material.material_name}: ₹{product_price}")
            return product_price

        print(f"Price not available for material: {material.material_name}")
        return None

    except Exception as e:
        print(f"Error calculating product price: {e}")
        return None
