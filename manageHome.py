from flask import Blueprint, render_template, flash, request, redirect, url_for
from models import db, HomeProduct, Products

manage_homeproducts = Blueprint('homeproduct', __name__)

# Route to display home products in the admin panel
@manage_homeproducts.route('/manage-homeproducts', methods=['POST'])
def show_homeproducts():
    home_products = HomeProduct.query.order_by(HomeProduct.homeProduct_id.asc()).all()  # Fetch all home products from the database
    products = Products.query.all()
    return render_template('mangeHome.html', home_products=home_products,products=products)

# Route to update home product's product_id
@manage_homeproducts.route('/update-homeproduct-productid/<int:homeProduct_id>', methods=['POST'])
def update_homeproduct_productid(homeProduct_id):
    new_product_id = request.form['product_id']  # Get the new product_id from the form
    home_product = HomeProduct.query.get(homeProduct_id)
    existing_product = HomeProduct.query.filter_by(product_id=new_product_id).first()

    if existing_product:
        flash(f"Product ID {new_product_id} is already assigned to another home product!", "danger")
        return show_homeproducts()
    
    if home_product:
        home_product.product_id = new_product_id
        db.session.commit()
        flash(f"HomeProduct ID {homeProduct_id} updated successfully to Product ID {new_product_id}.", "success")
    else:
        flash(f"No home product found with ID {homeProduct_id}.", "danger")
    updret=show_homeproducts()
    return updret

@manage_homeproducts.route('/delete-homeproduct/<int:homeProduct_id>', methods=['GET', 'POST'])
def delete_homeproduct(homeProduct_id):
    home_product = HomeProduct.query.get_or_404(homeProduct_id)  # Fetch the home product or return 404
    db.session.delete(home_product)  # Delete the home product
    db.session.commit()  # Save changes to the database
    flash(f'HomeProduct ID {homeProduct_id} deleted successfully!', 'success')

    # Instead of redirecting, re-render the template
    dltret=show_homeproducts()
    return dltret

@manage_homeproducts.route('/add-homeproduct', methods=['POST'])
def add_homeproduct():
    try:
        product_id = request.form['product_id']

        if not product_id:
            flash("Product ID is required.", "danger")
            addret=show_homeproducts()
            return addret

        # Check if product_id exists in the Products table
        product = Products.query.get(product_id)
        if not product:
            flash(f"Error: Product ID {product_id} does not exist.", "danger")
            addret=show_homeproducts()
            return addret
        
        existing_product = HomeProduct.query.filter_by(
            product_id=product_id
        ).first()

        if existing_product:
            addret=show_homeproducts()
            return addret

        # Create a new HomeProduct entry
        new_home_product = HomeProduct(product_id=product_id)
        db.session.add(new_home_product)
        db.session.commit()

        flash(f"Home Product with Product ID {product_id} added successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error adding home product: {str(e)}", "danger")

    addret=show_homeproducts()
    return addret


