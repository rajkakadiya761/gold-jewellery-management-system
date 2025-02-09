from flask import Blueprint, render_template, request, flash, redirect, session, url_for
from models import db, Products, Material, ProductMaterial

# Create Blueprint for product management
manage_products_bp = Blueprint('manage_products', __name__)

@manage_products_bp.route('/manage-products', methods=['POST'])
def manage_products():
    products = Products.query.all()  # Get all products
    materials = Material.query.all()  # Get all materials
    product_materials = ProductMaterial.query.all()  # Get all product-material relationships

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

    return render_template(
        'manageProducts.html',
        products=products,
        product_material_map=product_material_map,
        materials=materials
    )
    
@manage_products_bp.route('/add-product', methods=['POST'])
def add_product():
    try:
        name = request.form['name']
        description = request.form['description']
        product_weight = request.form['product_weight']
        category = request.form['category']
        photo1 = request.form['photo1']
        photo2 = request.form['photo2']
        material_id = request.form['material_id']
        sizes = request.form.getlist('sizes')  # Get all checked values
        if not sizes:
            sizes = ["medium"]

        size_str = ",".join(sizes)
        
        if not all([name, description, product_weight, size_str, category, photo1, photo2, material_id]):
            flash("All fields are required.", "danger")
            return redirect(url_for('manage_products.manage_products'))
        
        existing_product = Products.query.filter_by(
            name=name,
            description=description,
            product_weight=product_weight,
            sizes=size_str,
            category=category,
            photo1=photo1,
            photo2=photo2
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
            photo1=photo1,
            photo2=photo2
        )
        db.session.add(new_product)
        db.session.commit()  # Commit to generate product_id

        # Refresh the session to ensure product_id is updated
        db.session.refresh(new_product)

        print(f"New product_id: {new_product.product_id}")  # Debug log

        # Now add the material relationship (product_id -> material_id)
        product_material = ProductMaterial(product_id=new_product.product_id, material_id=material_id)
        db.session.add(product_material)
        db.session.commit()  # Commit the relationship


        flash("Product added successfully!", "success")
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
            # return redirect(url_for('manage_products.manage_products'))
            updret=manage_products()
            return updret
        
        new_weight = request.form.get('product_weight', '').strip()  # Strip spaces

        # Ensure new_weight is a valid number
        if new_weight and new_weight.replace('.', '', 1).isdigit():
            new_weight = float(new_weight)
            if new_weight > 0:  # Only update if weight is positive
                product.product_weight = new_weight
            else:
                flash("Weight cannot be zero or negative! Keeping the previous weight.", "warning")

        # Update product details
        product.name = request.form['name']
        product.description = request.form['description']
        product.product_weight = request.form['product_weight']
        product.category = request.form['category']
        product.photo1 = request.form['photo1']
        product.photo2 = request.form['photo2']

        # Update material-product relationship
        material_id = request.form['material_id']
        product_material = ProductMaterial.query.filter_by(product_id=product_id).first()
       
        selected_sizes = request.form.getlist('sizes')  # Ensure correct name is used
        if not selected_sizes:
            selected_sizes = ["medium"]

        product.sizes = ",".join(selected_sizes)  # Convert list to string
        
        if product_material:
            product_material.material_id = material_id
        material_id = request.form.get('material_id')  # Use .get() to avoid KeyError
        
        db.session.commit()
        flash("Product updated successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error updating product: {str(e)}", "danger")

    # return redirect(url_for('manage_products.manage_products'))
    updret=manage_products()
    return updret

@manage_products_bp.route('/delete-product/<int:product_id>', methods=['GET'])
def delete_product(product_id):
    try:
        # Delete product-material relationships first
        ProductMaterial.query.filter_by(product_id=product_id).delete()

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