from flask import Blueprint, render_template, request,redirect, url_for, flash
from models import db, Products,Material,ProductMaterial

# Create Blueprint for product management
product_bp_ring = Blueprint('productFinger', __name__)

@product_bp_ring.route('/ring')
def show_rings():
    material = request.args.get('material', 'all')  # Default to 'all' if no material is selected
    
    if material == 'all':
        rings = Products.query.filter_by(category='ring').all()
    else:
        # Get the material object based on the selected material name (Gold, Silver, Platinum)
        material_obj = Material.query.filter_by(material_name=material).first()  # Use 'material_name' here
        
        if material_obj:
            material_id = material_obj.material_id  # Use 'material_id' here, not 'id'
            
            # Get earrings that have the selected material through the ProductMaterial relation
            rings = db.session.query(Products).join(ProductMaterial).filter(
                Products.category == 'ring', ProductMaterial.material_id == material_id
            ).all()
        else:
            # If no material found, show an empty list or handle as needed
            rings = []

    return render_template('ring.html', rings=rings, material=material)


@product_bp_ring.route('/delete-ring/<int:product_id>', methods=['GET'])
def delete_ring(product_id):
    try:
        product = Products.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
            flash("Product deleted successfully!", "success")
        else:
            flash("Product not found.", "danger")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting product: {str(e)}", "danger")

    rings = Products.query.filter_by(category='ring').all()
    return render_template('ring.html', rings=rings)  

@product_bp_ring.route('/ring/<int:product_id>')
def ring_details(product_id):
    # Fetch the product from the database
    earring = Products.query.get_or_404(product_id)
    return render_template('earring_details.html', earring=earring)
