from flask import Blueprint, render_template, request, flash
from models import ProductPricing, db, Products, Material, ProductMaterial

# Create Blueprint for male Collection
product_bp_male = Blueprint('productMale', __name__)

@product_bp_male.route('/male-collection')
def show_male_products():
    material = request.args.get('material', 'all')  # Default to 'all'
    genders = request.args.getlist('gender')  # Fetch multiple gender values

    # Ensure at least Male and Uni are included if no gender is passed
    if not genders:
        genders = ['Male', 'Uni']

    if material == 'all':
        # Fetch products with Gender = Male or Uni
        products = Products.query.filter(Products.Gender.in_(genders)).all()
    else:
        material_obj = Material.query.filter_by(material_name=material).first()
        
        if material_obj:
            material_id = material_obj.material_id  # Get material ID
            
            # Fetch products with Male/Uni gender and selected material
            products = db.session.query(Products).join(ProductMaterial).filter(
                Products.Gender.in_(genders), ProductMaterial.material_id == material_id
            ).all()
        else:
            products = []

    return render_template('MaleCollec.html', products=products, material=material)


@product_bp_male.route('/delete-male-product/<int:product_id>', methods=['GET'])
def delete_male_product(product_id):
    try:
        product = Products.query.get(product_id)
        if product and product.Gender in ['Male', 'Uni']:  # Allow deletion for Male + Uni
            db.session.delete(product)
            db.session.commit()
            flash("Product deleted successfully!", "success")
        else:
            flash("Product not found or does not belong to the Male/Unisex collection.", "danger")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting product: {str(e)}", "danger")

    # Fetch updated list of Male + Unisex products
    products = Products.query.filter(Products.Gender.in_(['Male', 'Uni'])).all()
    return render_template('MaleCollec.html', products=products)

@product_bp_male.route('/products')
def show_products():
    material = request.args.get('material', 'all')
    genders = request.args.getlist('Gender')  # Get multiple Gender values (Male & Uni)

    query = Products.query.filter(Products.Gender.in_(genders))  # Filter for Male & Uni

    if material != 'all':
        material_obj = Material.query.filter_by(material_name=material).first()
        if material_obj:
            query = query.join(ProductMaterial).filter(ProductMaterial.material_id == material_obj.material_id)

    products = query.all()
    
    return render_template('MaleCollec.html', products=products, material=material)

@product_bp_male.route('/male-product/<int:product_id>')
def male_product_details(product_id):    
    earring = Products.query.get_or_404(product_id)
    price = ProductPricing.query.filter_by(product_id=product_id).first()  # Safer approach

    return render_template('earring_details.html', earring=earring, price=price)
