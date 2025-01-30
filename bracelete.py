from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Products,Material,ProductMaterial

# Create Blueprint for product management
product_bp_bracelete = Blueprint('productHand', __name__)

@product_bp_bracelete.route('/bracelete')
def show_braceletes():
    material = request.args.get('material', 'all')  # Default to 'all' if no material is selected
    
    if material == 'all':
        # Show all earrings regardless of material
        braceletes = Products.query.filter_by(category='bracelete').all()
    else:
        # Get the material object based on the selected material name (Gold, Silver, Platinum)
        material_obj = Material.query.filter_by(material_name=material).first()  # Use 'material_name' here
        
        if material_obj:
            material_id = material_obj.material_id  # Use 'material_id' here, not 'id'
            
            # Get earrings that have the selected material through the ProductMaterial relation
            braceletes = db.session.query(Products).join(ProductMaterial).filter(
                Products.category == 'bracelete', ProductMaterial.material_id == material_id
            ).all()
        else:
            # If no material found, show an empty list or handle as needed
            braceletes = []

    return render_template('bracelete.html', braceletes=braceletes, material=material)


@product_bp_bracelete.route('/delete-bracelete/<int:product_id>', methods=['GET'])
def delete_bracelete(product_id):
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

    braceletes = Products.query.filter_by(category='bracelete').all()
    return render_template('bracelete.html', braceletes=braceletes)  

@product_bp_bracelete.route('/bracelete/<int:product_id>')
def bracelete_details(product_id):
    # Fetch the product from the database
    earring = Products.query.get_or_404(product_id)
    return render_template('earring_details.html', earring=earring)
