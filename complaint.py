from flask import Blueprint, render_template, flash, request, redirect, url_for,session
from models import db, Complaints,Products,HomeProduct, ProductPricing,Payment

manage_complaints = Blueprint('complaint', __name__)

@manage_complaints.route('/file-complaint', methods=['POST'])
def file_complaint():
    if 'user_id' not in session:
        flash("You must be logged in to file a complaint", "danger")
        home_products = db.session.query(HomeProduct, Products, ProductPricing).\
            join(Products, HomeProduct.product_id == Products.product_id).\
            outerjoin(ProductPricing, Products.product_id == ProductPricing.product_id).all()
        return render_template("home.html", home_products=home_products)

    if request.method == 'POST':
        user_id = session['user_id']
        message = request.form['message']
        complaint_type = request.form['type']
        order_id = request.form['order_id']  # Fetch order_id from form

        # Fetch user_id from payments table based on order_id
        payment_record = db.session.query(Payment).filter_by(order_id=order_id).first()

        if payment_record:
            # Check if the user_id from payments matches the logged-in user
            if payment_record.user_id == user_id:
                # Create and save new complaint
                new_complaint = Complaints(user_id=user_id, message=message, type=complaint_type, order_id=order_id)
                db.session.add(new_complaint)
                db.session.commit()
                flash("Complaint filed successfully!", "success")
            else:
                flash("No such order ID found for your account.", "danger")
        else:
            flash("No such order ID found.", "danger")

        home_products = db.session.query(HomeProduct, Products, ProductPricing).\
            join(Products, HomeProduct.product_id == Products.product_id).\
            outerjoin(ProductPricing, Products.product_id == ProductPricing.product_id).all()
        
        return render_template("home.html", home_products=home_products)

# Route to display complaints in the admin panel
@manage_complaints.route('/manage-complaints', methods=['POST'])
def show_complaints():
    complaints = Complaints.query.all()  # Fetch all complaints from the database
    return render_template('manageComplaints.html', complaints=complaints)

# Route to update complaint status
@manage_complaints.route('/update-complaint-status/<int:complaint_id>', methods=['POST'])
def update_complaint_status(complaint_id):
    new_status = request.form['status']  # Get the status from the form
    complaint = Complaints.query.get(complaint_id)
    if complaint:
        complaint.status = new_status
        db.session.commit()
        flash(f"Complaint ID {complaint_id} updated successfully to '{new_status}'.", "success")
    else:
        flash(f"No complaint found with ID {complaint_id}.", "danger")
    complaints = Complaints.query.all()
    return render_template('manageComplaints.html', complaints=complaints)

@manage_complaints.route('/delete-complaint/<int:complaint_id>', methods=['POST'])
def delete_complaint(complaint_id):
    complaint = Complaints.query.get_or_404(complaint_id)  # Fetch the complaint or return 404
    db.session.delete(complaint)  # Delete the complaint
    db.session.commit()  # Save changes to the database
    flash(f'Complaint ID {complaint_id} deleted successfully!', 'success')
    return redirect(url_for('complaint.show_complaints'))
