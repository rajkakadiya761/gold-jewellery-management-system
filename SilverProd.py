from flask import Blueprint, render_template, request, flash
from models import ProductPricing, db, Products, Material, ProductMaterial

# Create Blueprint for Silver Collection
product_bp_silver = Blueprint('productSilver', __name__)

@product_bp_silver.route('/silver-collection')
def show_silver_products():
    # Get material ID for "Silver" (material_id = 1)
    material_silver = Material.query.filter_by(material_name="Silver").first()

    if material_silver:
        material_id = material_silver.material_id  # Get Silver material ID

        # Fetch all products that have material_id = 1 (Silver) from ProductMaterial table
        products = db.session.query(Products).join(ProductMaterial).filter(
            ProductMaterial.material_id == material_id
        ).all()
    else:
        products = []

    return render_template('SilverProd.html', products=products)


@product_bp_silver.route('/delete-silver-product/<int:product_id>', methods=['GET'])
def delete_silver_product(product_id):
    try:
        product = Products.query.get(product_id)
        material_silver = Material.query.filter_by(material_name="Silver").first()

        if product and material_silver:
            # Check if product has material silver in ProductMaterial table
            has_silver = db.session.query(ProductMaterial).filter_by(
                product_id=product_id, material_id=material_silver.material_id
            ).first()

            if has_silver:
                db.session.delete(product)
                db.session.commit()
                flash("silver product deleted successfully!", "success")
            else:
                flash("Product is not made of silver.", "danger")
        else:
            flash("Product not found.", "danger")

    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting product: {str(e)}", "danger")

    return show_silver_products()


@product_bp_silver.route('/silver-product/<int:product_id>')
def silver_product_details(product_id):    
    earring = Products.query.get_or_404(product_id)
    price = ProductPricing.query.filter_by(product_id=product_id).first()  # Safer approach

    return render_template('earring_details.html', earring=earring, price=price)