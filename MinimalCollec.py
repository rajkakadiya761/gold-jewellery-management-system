from flask import Blueprint, render_template, request, flash
from models import Products, db, ProductMaterial, Material, ProductPricing

# Create Blueprint for Minimal Collection
product_bp_minimal = Blueprint('productMinimal', __name__)

@product_bp_minimal.route('/minimal-collection')
def show_minimal_products():
   material_filter = request.args.get('material', 'all')  # Get selected material

    # Base query: Fetch all products where Occasion is "Minimal"
   query = Products.query.filter_by(Occasion="Minimal")

   if material_filter != 'all':  # Apply material filter if not "all"
        query = query.join(ProductMaterial).join(Material).filter(Material.material_name == material_filter)

   products = query.all()

   return render_template('MinimalCollec.html', products=products)


@product_bp_minimal.route('/delete-minimal-product/<int:product_id>', methods=['GET'])
def delete_minimal_product(product_id):
    try:
        product = Products.query.get(product_id)

        if product and product.Occasion == "Minimal":
            db.session.delete(product)
            db.session.commit()
            flash("Minimal product deleted successfully!", "success")
        else:
            flash("Product not found or is not a Minimal product.", "danger")

    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting product: {str(e)}", "danger")

    return show_minimal_products()


@product_bp_minimal.route('/minimal-product/<int:product_id>')
def minimal_product_details(product_id):    
    earring = Products.query.get_or_404(product_id)
    price = ProductPricing.query.filter_by(product_id=product_id).first()  # Safer approach

    return render_template('earring_details.html', earring=earring, price=price)