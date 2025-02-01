from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify
from models import db, Products,Material,ProductMaterial

# Create Blueprint for product management
product_bp = Blueprint('product', __name__)

@product_bp.route('/earrings')
def show_earrings():
    material = request.args.get('material', 'all')  # Default to 'all' if no material is selected
    
    if material == 'all':
        # Show all earrings regardless of material
        earrings = Products.query.filter_by(category='earrings').all()
    else:
        # Get the material object based on the selected material name (Gold, Silver, Platinum)
        material_obj = Material.query.filter_by(material_name=material).first()  # Use 'material_name' here
        
        if material_obj:
            material_id = material_obj.material_id  # Use 'material_id' here, not 'id'
            
            # Get earrings that have the selected material through the ProductMaterial relation
            earrings = db.session.query(Products).join(ProductMaterial).filter(
                Products.category == 'earrings', ProductMaterial.material_id == material_id
            ).all()
        else:
            # If no material found, show an empty list or handle as needed
            earrings = []

    return render_template('earrings.html', earrings=earrings, material=material)


@product_bp.route('/delete-earring/<int:product_id>', methods=['GET'])
def delete_earring(product_id):
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

    earrings = Products.query.filter_by(category='earring').all()
    return render_template('earrings.html', earrings=earrings)  

@product_bp.route('/earring/<int:product_id>')
def earring_details(product_id):
    # Fetch the product from the database
    earring = Products.query.get_or_404(product_id)
    return render_template('earring_details.html', earring=earring)



