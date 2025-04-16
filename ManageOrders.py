from flask import Blueprint, render_template, flash, request, redirect, url_for, session
from models import db, Payments, Address

manage_payments = Blueprint('payment', __name__)

# Route to show payment info along with address for the logged-in user
@manage_payments.route('/show_payments', methods=['POST'])
def show_payments():

    # Show ALL payments with their address (for admin)
    all_payments = db.session.query(Payments, Address)\
        .join(Address, Payments.user_id == Address.user_id)\
        .all()

    print("Fetched payments:", all_payments)  
    return render_template("ManageOrders.html", all_payments=all_payments)

# Optional: Admin route to view all users' payments with addresses
@manage_payments.route('/manage-payments', methods=['GET'])
def admin_view_payments():
    # Fetch all payment records and associated addresses
    all_payments = db.session.query(Payments, Address).join(Address, Payments.user_id == Address.user_id).all()

    return render_template("ManageOrders.html", all_payments=all_payments)
