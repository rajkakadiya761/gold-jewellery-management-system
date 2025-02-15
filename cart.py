from flask import Blueprint, render_template, flash, request, session, jsonify,redirect, url_for
from models import ProductPricing, db,Users,Products,Cart,HomeProduct

manage_Cart = Blueprint('Cart', __name__)

@manage_Cart.route('/cart', methods=['GET'])
def view_cart():
    if 'user_id' not in session:
        flash('Please log in to add items to your cart')
        home_products = (
        db.session.query(HomeProduct, Products, ProductPricing)
       .join(Products, HomeProduct.product_id == Products.product_id)
       .join(ProductPricing, Products.product_id == ProductPricing.product_id)
       .all()
       ) 
        return render_template("home.html", home_products=home_products)

    user_id = session['user_id']
    cart = Cart.query.filter_by(user_id=user_id).first()

    if cart and cart.product_ids:
        # Convert comma-separated product IDs to a list
        product_ids = cart.product_ids.split(',')

        # Fetch product details along with their prices and quantities
        cart_items = (
            db.session.query(Products, ProductPricing)
            .join(ProductPricing, Products.product_id == ProductPricing.product_id)
            .filter(Products.product_id.in_(product_ids))
            .all()
        )

        # Prepare the data for rendering
        items_with_details = [
            {
                "product_id": product.product_id,
                "name": product.name,
                "description": product.description,
                "photo1": product.photo1,
                "price": pricing.price,
                "quantity": pricing.quantity,
            }
            for product, pricing in cart_items
        ]

        return render_template('cart.html', cart_items=items_with_details)
    else:
        return render_template('cart.html', cart_items=[])



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
    
    if not cart or not cart.product_ids:
        return jsonify({"error": "Cart not found"}), 404

    product_ids_list = cart.product_ids.split(',')
    
    if str(product_id) in product_ids_list:
        product_ids_list.remove(str(product_id))  # Remove the product_id
        cart.product_ids = ','.join(product_ids_list)  # Update the cart with the new list
        db.session.commit()
        return jsonify({"message": "Item removed from cart"}), 200
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



