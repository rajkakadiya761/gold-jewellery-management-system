from flask import Blueprint, render_template, request, flash
from models import Products, db, ProductMaterial, Material, ProductPricing

# Create Blueprint for Wedding Collection
product_bp_wedding = Blueprint('productWedding', __name__)

@product_bp_wedding.route('/wedding-collection')
def show_wedding_products():
   material_filter = request.args.get('material', 'all')  # Get selected material

    # Base query: Fetch all products where Occasion is "Wedding"
   query = Products.query.filter_by(Occasion="Wedding")

   if material_filter != 'all':  # Apply material filter if not "all"
        query = query.join(ProductMaterial).join(Material).filter(Material.material_name == material_filter)

   products = query.all()

   return render_template('WeddingCollec.html', products=products)


@product_bp_wedding.route('/delete-wedding-product/<int:product_id>', methods=['GET'])
def delete_wedding_product(product_id):
    try:
        product = Products.query.get(product_id)

        if product and product.Occasion == "Wedding":
            db.session.delete(product)
            db.session.commit()
            flash("Wedding product deleted successfully!", "success")
        else:
            flash("Product not found or is not a Wedding product.", "danger")

    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting product: {str(e)}", "danger")

    return show_wedding_products()


@product_bp_wedding.route('/wedding-product/<int:product_id>')
def wedding_product_details(product_id):    
    earring = Products.query.get_or_404(product_id)
    price = ProductPricing.query.filter_by(product_id=product_id).first()  

    return render_template('earring_details.html', earring=earring, price=price)