from flask import Blueprint, render_template, flash, request, session, jsonify,redirect, url_for
from models import db,Users,Products,Cart

manage_Cart = Blueprint('Cart', __name__)

@manage_Cart.route('/cart', methods=['GET'])
def view_cart():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please log in to add items to your cart.'}), 401

    user_id = session['user_id']
    cart = Cart.query.filter_by(user_id=user_id).first()
    
    if cart:
        # Fetch product details for each product_id in the cart
        product_ids = cart.product_ids.split(',')
        products = Products.query.filter(Products.product_id.in_(product_ids)).all()
        
        # Pass the products to the template
        return render_template('cart.html', cart_items=products)
    else:
        return render_template('cart.html', cart_items=[])  # Render with an empty cart


@manage_Cart.route('/add_to_cart', methods=['POST'])
def add_product_to_cart():
    # Get product_id from the request data (use .get() for safe access)
    product_id = request.form.get('product_id')
    user_id = session.get('user_id')  # Assuming user is logged in
    
    if not user_id:
        return jsonify({"error": "User not logged in"}), 401

    # Check if cart exists for the user
    cart = Cart.query.filter_by(user_id=user_id).first()
    
    if cart:
        # If cart exists, add product_id if not already present
        product_ids_list = cart.product_ids.split(',') if cart.product_ids else []
        
        if str(product_id) not in product_ids_list:
            cart.product_ids += f',{product_id}' if cart.product_ids else str(product_id)
            db.session.commit()
    else:
        # If no cart exists, create a new cart entry with the product_id
        new_cart = Cart(user_id=user_id, product_ids=str(product_id))
        db.session.add(new_cart)
        db.session.commit()

    return jsonify({"status": "success", "message": "Product added to cart."})


@manage_Cart.route('/remove-from-cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    """Removes a product from the cart of the logged-in user."""
    if 'user_id' not in session:
        return jsonify({"error": "User not logged in"}), 401

    user_id = session['user_id']
    cart = Cart.query.filter_by(user_id=user_id).first()
    
    if not cart:
        return jsonify({"error": "Cart not found"}), 404

    # Remove product_id from the cart's product_ids
    product_ids_list = cart.product_ids.split(',')
    
    if str(product_id) in product_ids_list:
        product_ids_list.remove(str(product_id))  # Remove the product_id
        cart.product_ids = ','.join(product_ids_list)  # Update the cart with the new list
        db.session.commit()
        return jsonify({"message": "Item removed from cart"})
    else:
        return jsonify({"error": "Product not found in cart"}), 404


@manage_Cart.route('/manage-cart', methods=['POST'])
def manage_carts():
    carts = Cart.query.all()  # Fetch all cart entries

    cart_data = []
    for cart in carts:
        cart_data.append({
            "cart_id": cart.cart_id,
            "user_id": cart.user.user_id if cart.user else "Unable to fetch",
            "product_ids": cart.product_ids if cart.product_ids else "No products"
        })

    return render_template(
        'viewCart.html',
        carts=cart_data
    )



