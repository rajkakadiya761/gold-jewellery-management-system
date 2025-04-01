from flask import Blueprint, render_template, request, flash
from models import ProductPricing, db, Products, Material, ProductMaterial

# Create Blueprint for Platinum Collection
product_bp_platinum = Blueprint('productPlatinum', __name__)

@product_bp_platinum.route('/platinum-collection')
def show_platinum_products():
    # Get material ID for "Platinum" (material_id = 3)
    material_platinum = Material.query.filter_by(material_name="Platinum").first()

    if material_platinum:
        material_id = material_platinum.material_id  # Get Platinum material ID

        # Fetch all products that have material_id = 1 (Platinum) from ProductMaterial table
        products = db.session.query(Products).join(ProductMaterial).filter(
            ProductMaterial.material_id == material_id
        ).all()
    else:
        products = []

    return render_template('PlatinumProd.html', products=products)


@product_bp_platinum.route('/delete-platinum-product/<int:product_id>', methods=['GET'])
def delete_platinum_product(product_id):
    try:
        product = Products.query.get(product_id)
        material_platinum = Material.query.filter_by(material_name="Platinum").first()

        if product and material_platinum:
            # Check if product has material platinum in ProductMaterial table
            has_platinum = db.session.query(ProductMaterial).filter_by(
                product_id=product_id, material_id=material_platinum.material_id
            ).first()

            if has_platinum:
                db.session.delete(product)
                db.session.commit()
                flash("platinum product deleted successfully!", "success")
            else:
                flash("Product is not made of platinum.", "danger")
        else:
            flash("Product not found.", "danger")

    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting product: {str(e)}", "danger")

    return show_platinum_products()


@product_bp_platinum.route('/platinum-product/<int:product_id>')
def platinum_product_details(product_id):    
    earring = Products.query.get_or_404(product_id)
    price = ProductPricing.query.filter_by(product_id=product_id).first()  # Safer approach

    return render_template('earring_details.html', earring=earring, price=price)