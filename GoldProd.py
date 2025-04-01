from flask import Blueprint, render_template, request, flash
from models import ProductPricing, db, Products, Material, ProductMaterial

# Create Blueprint for Gold Collection
product_bp_gold = Blueprint('productGold', __name__)

@product_bp_gold.route('/gold-collection')
def show_gold_products():
    # Get material ID for "Gold" (material_id = 1)
    material_gold = Material.query.filter_by(material_name="Gold").first()

    if material_gold:
        material_id = material_gold.material_id  # Get Gold material ID

        # Fetch all products that have material_id = 1 (Gold) from ProductMaterial table
        products = db.session.query(Products).join(ProductMaterial).filter(
            ProductMaterial.material_id == material_id
        ).all()
    else:
        products = []

    return render_template('GoldProd.html', products=products)


@product_bp_gold.route('/delete-gold-product/<int:product_id>', methods=['GET'])
def delete_gold_product(product_id):
    try:
        product = Products.query.get(product_id)
        material_gold = Material.query.filter_by(material_name="Gold").first()

        if product and material_gold:
            # Check if product has material Gold in ProductMaterial table
            has_gold = db.session.query(ProductMaterial).filter_by(
                product_id=product_id, material_id=material_gold.material_id
            ).first()

            if has_gold:
                db.session.delete(product)
                db.session.commit()
                flash("Gold product deleted successfully!", "success")
            else:
                flash("Product is not made of Gold.", "danger")
        else:
            flash("Product not found.", "danger")

    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting product: {str(e)}", "danger")

    return show_gold_products()


@product_bp_gold.route('/gold-product/<int:product_id>')
def gold_product_details(product_id):    
    earring = Products.query.get_or_404(product_id)
    price = ProductPricing.query.filter_by(product_id=product_id).first()  # Safer approach

    return render_template('earring_details.html', earring=earring, price=price)