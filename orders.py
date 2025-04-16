from flask import Blueprint, request, jsonify, session 
from models import Address, db ,Products,Payments,ProductPricing
from datetime import datetime
import razorpay

# ✅ Blueprint for managing addresses
manage_address = Blueprint('address_bp', __name__)

 # ✅ Razorpay Configuration (Directly in `app.py`)
# RAZORPAY_KEY_ID = "rzp_test_rrFzDrB1DENkoe"          # Replace with your test key
# RAZORPAY_KEY_SECRET = "snJcm8lGUk6dTxTTYGvAYeTx"    # Replace with your test secret

razorpay_client = razorpay.Client(auth=("rzp_test_rrFzDrB1DENkoe", "snJcm8lGUk6dTxTTYGvAYeTx"))


# ✅ Fetch the saved address by `user_id` only
@manage_address.route('/get_address', methods=['GET'])
def get_user_address():
    """Fetch the saved address by `user_id` only."""

    print("Session user_id:", session.get('user_id'))
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401

    # ✅ Fetch the address using `user_id` only
    address = Address.query.filter_by(user_id=user_id).first()

    


    if address:
        return jsonify({
            'address_id': address.address_id,
            'address': address.address,
            'state': address.state,
            'city': address.city,
            'postal_code': address.postal_code,
            'phone_number': address.phone_number,
            'exists': True
        }), 200
    else:
        # ✅ Send empty fields if no address exists
        return jsonify({
            'address_id': None,
            'address': '',
            'state': '',
            'city': '',
            'postal_code': '',
            'phone_number': '',
            'exists': False
        }), 200

# ✅ **Save or Update Address Route**


@manage_address.route('/save_address', methods=['POST'])
def save_address():
    """Save or update the address based on `user_id` only."""
    
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401

    data = request.get_json()

    # ✅ Check if the user already has an address
    existing_address = Address.query.filter_by(user_id=user_id).first()

    if existing_address:
        # ✅ Update the existing address
        existing_address.address = data.get('address')
        existing_address.state = data.get('state')
        existing_address.city = data.get('city')
        existing_address.postal_code = data.get('postal_code')
        existing_address.phone_number = data.get('phone_number')
        message = "Address updated successfully!"
    else:
        # ✅ Create a new address record
        new_address = Address(
            user_id=user_id,
            address=data.get('address'),
            state=data.get('state'),
            city=data.get('city'),
            postal_code=data.get('postal_code'),
            phone_number=data.get('phone_number')
        )
        db.session.add(new_address)
        message = "Address added successfully!"

    # ✅ Commit the changes
    try:
        db.session.commit()
        return jsonify({'message': message}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to save address: {str(e)}'}), 500
    
@manage_address.route('/initiate_payment', methods=['POST'])
def initiate_payment():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401

    data = request.get_json()
    print("Received Data:", data)

    product_ids = data.get('product_ids', [])
    quantities = data.get('quantities', [])

    if not product_ids or not isinstance(product_ids, list):
        return jsonify({'error': 'Product IDs are required as a list'}), 400
    if not quantities or not isinstance(quantities, list) or len(quantities) != len(product_ids):
        return jsonify({'error': 'Quantities must match product IDs'}), 400

    total_price = 0
    valid_product_ids = []
    valid_quantities = []

    for product_id, quantity in zip(product_ids, quantities):
        product = Products.query.filter_by(product_id=product_id).first()
        product_pricing = ProductPricing.query.filter_by(product_id=product_id).first()

        if not product or not product_pricing or product_pricing.price <= 0:
            return jsonify({'error': f'Invalid product or price for ID {product_id}'}), 400

        valid_product_ids.append(str(product_id))
        valid_quantities.append(quantity)
        total_price += product_pricing.price * quantity

    if not valid_product_ids:
        return jsonify({'error': 'No valid products for payment'}), 400

    amount = int(total_price * 100)
    product_ids_str = ','.join(valid_product_ids)  # ✅ stringify for Razorpay

    try:
        order_data = {
            'amount': amount,
            'currency': 'INR',
            'receipt':product_ids_str,
            'notes': {'product_ids': product_ids_str}
        }

        razorpay_order = razorpay_client.order.create(data=order_data)
        print("📦 Razorpay Order Response:", razorpay_order)

        if razorpay_order.get('status') == 'created':
            try:
                # new_payment = Payments(
                #     user_id=user_id,
                #     product_ids=valid_product_ids,
                #     quantities=valid_quantities,  # ✅ Store quantities correctly
                #     price=round(total_price, 2),
                #     transaction_id=razorpay_order['id']
                # )
                # db.session.add(new_payment)
                # db.session.commit()
                print("✅ Payment saved to DB")
            except Exception as db_err:
                print("❌ Error saving payment:", db_err)
                return jsonify({'error': 'Failed to save payment to database'}), 500

            return jsonify({
                'order_id': razorpay_order['id'],
                'amount': razorpay_order['amount'],
                'currency': razorpay_order['currency']
            }), 200

        return jsonify({'error': 'Razorpay order creation failed'}), 500

    except Exception as e:
        print("❌ Error in /initiate_payment:", str(e))
        return jsonify({'error': 'Something went wrong during payment initiation'}), 500


    
@manage_address.route('/payment_success', methods=['POST'])
def payment_success():
    data = request.get_json()
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401

    try:
        new_payment = Payments(
            user_id=user_id,
            product_ids=data['product_ids'],
            quantities=data['quantities'],
            price=data['price'],
            transaction_id=data['transaction_id']
        )
        db.session.add(new_payment)
        db.session.commit()
        return jsonify({'message': 'Payment recorded successfully'}), 200
    except Exception as e:
        print("❌ Error saving successful payment:", str(e))
        return jsonify({'error': 'Failed to save payment'}), 500
