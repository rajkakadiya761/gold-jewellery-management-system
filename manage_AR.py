from flask import Blueprint, render_template, flash, request, redirect, url_for
from models import db, ProcessedImage, Products
from sqlalchemy import text 

# Create a Blueprint for managing processed images
manage_images_bp = Blueprint('manage_images', __name__)

@manage_images_bp.route('/manage-images', methods=['GET','POST'])
def manage_images():
    images = ProcessedImage.query.all()

    # Fetch available products that are not already associated with an image
    query = text("SELECT product_id, name FROM products WHERE product_id NOT IN (SELECT product_id FROM processed_images)")
    available_products = db.session.execute(query).fetchall()

    # Extract product IDs from query result
    available_products = [{"id": row[0], "name": row[1]} for row in available_products]

    # Debugging: Print to console
    print("Available Products:", available_products)

    return render_template('manageAR.html', images=images, available_products=available_products)

@manage_images_bp.route('/add_image', methods=['POST'])
def add_image():
    try:
        product_id = request.form['product_id']
        png_image = request.form['png_image']
        
        new_image = ProcessedImage(product_id=product_id, png_image=png_image)
        
        db.session.add(new_image)
        db.session.commit()
        
        flash('Image added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding image: {str(e)}', 'danger')

    return redirect(url_for('manage_images.manage_images'))

@manage_images_bp.route('/manage-images/update_image/<int:png_id>', methods=['POST'])
def update_image(png_id):
    try:
        product_id = request.form['product_id']
        png_image = request.form['png_image']
        
        image = ProcessedImage.query.get(png_id)
        if not image:
            flash('Image not found.', 'danger')
            return redirect(url_for('manage_images.manage_images'))
        
        image.product_id = product_id
        image.png_image = png_image
        
        db.session.commit()
        flash('Image updated successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating image: {str(e)}', 'danger')

    return redirect(url_for('manage_images.manage_images'))

@manage_images_bp.route('/delete_image/<int:png_id>', methods=['GET'])
def delete_image(png_id):
    try:
        image = ProcessedImage.query.get(png_id)
        if image:
            db.session.delete(image)
            db.session.commit()
            flash('Image deleted successfully.', 'success')
        else:
            flash('Image not found.', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting image: {str(e)}', 'danger')

    return redirect(url_for('manage_images.manage_images'))
