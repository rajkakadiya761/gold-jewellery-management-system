from flask import Flask, render_template, request, flash, url_for,session, redirect
from markupsafe import Markup
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from manage_users import manage_users_bp  # Import the Blueprint
from complaint import manage_complaints
from models import HomeProduct, Products, db, Users , Complaints 
from priceAPI import make_gapi_request
from manage_products import manage_products_bp
from earrings import product_bp
from necklace import product_bp_necklace
from bracelete import product_bp_bracelete
from ring import product_bp_ring
from feedback import manage_feedbacks
from cart import manage_Cart
from manageHome import manage_homeproducts

db = db  # ORM setup
mail = Mail()  # Email setup

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/arihant'  # Replace password if applicable
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Replace with your mail server
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'krisha4801@gmail.com'  # Replace with your email
    app.config['MAIL_PASSWORD'] = 'khmg oflh ddyq oxey'  # Replace with your email password
    app.config['SECRET_KEY'] = 'your_secret_key_here'

    # Initialize extensions with the app
    db.init_app(app)
    mail.init_app(app)
    
    # Register blueprints
    app.register_blueprint(manage_users_bp)
    app.register_blueprint(manage_complaints)
    app.register_blueprint(manage_products_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(product_bp_necklace)
    app.register_blueprint(product_bp_bracelete)
    app.register_blueprint(product_bp_ring)
    app.register_blueprint(manage_feedbacks)
    app.register_blueprint(manage_Cart)
    app.register_blueprint(manage_homeproducts)


    # Route for Home Page
    @app.route("/")
    def page1():
      metal_prices = make_gapi_request()
      home_products = db.session.query(HomeProduct, Products).join(Products).all() 
      return render_template("home.html", XAU=metal_prices['XAU'], XAG=metal_prices['XAG'], XPT=metal_prices['XPT'], home_products=home_products)    

    # Login route to handle the login form submission
    @app.route('/login', methods=['POST'])
    def login():
        email = request.form['logInEmail']
        password = request.form['logInPassword']

        # Query the database to find the user with the entered email
        user = Users.query.filter_by(email=email).first()

        # Check if the user exists and if the password matches
        if user and user.password == password:
            if user.is_confirmed:
                if user and user.password == password and user.role=="Customer":
                    session['user_id'] = user.user_id
                    flash(f"{user.name} from {user.email} Login is Successful!", "success")  # Flash success message
                elif user and user.password == password and user.role=="Admin":
                      return render_template('admin.html')
            else:
                link = Markup(
                    'Please confirm Email Verification Link! '
                    '<a href="{}">Click here</a> if you want the link to be re-sent.'.format(url_for('resend_confirmation', email=email))
                )
                flash(link, "danger")
        else:
            flash("Login Failed! Invalid email or password.", "danger")  # Flash error message
        
        return render_template("home.html")  # Stay on the same page and display the flash message
    
    @app.route('/forgot-password', methods=['GET'])
    def forgotPassword():
        email = request.args.get('email')
        token = generate_confirmation_token(email)
        confirm_url = url_for('pass_reset', token=token, _external=True)
        subject = "Forgot Password - Email Confirmation"
        body = f"""
        Please confirm your forget password request by clicking the link below:
        {confirm_url}
        """

        try:
            msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[email], body=body)
            mail.send(msg)
            flash("Please confirm forget password link sent to your email", "success")
        except Exception as e:
            print(f"Error sending email: {e}") 
        return render_template("home.html")

    @app.route('/resend-confirmation')
    def resend_confirmation():
        email = request.args.get('email')
        if email:
            send_confirmation_email(email)
            flash("Verification email has been sent.", "success")
        else:
            flash("Invalid email address.", "danger")
        return render_template("home.html")  # Redirect or render an appropriate template

    # Generate a secure token
    def generate_confirmation_token(email):
        serializer = URLSafeTimedSerializer(app.secret_key)
        return serializer.dumps(email, salt='email-confirmation-salt')

    # Send confirmation email
    def send_confirmation_email(email):
        token = generate_confirmation_token(email)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        subject = "Please confirm your email"
        body = f"""
        Welcome! Thanks for signing up. Please confirm your email by clicking the link below:
        {confirm_url}
        """

        try:
            msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[email], body=body)
            mail.send(msg)
        except Exception as e:
            print(f"Error sending email: {e}")  # Replace with proper logging in production

    @app.route('/signup', methods=['POST'])
    def signUp():
        name = request.form['signupName']
        email = request.form['signupEmail']
        password = request.form['signupPassword']

        # Check if email already exists
        existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already exists. Please use a different email.", "danger")
            return render_template("home.html")

        # Create a new user
        new_user = Users(name=name, email=email, password=password, role="Customer")
        db.session.add(new_user)
        db.session.commit()

        # Send confirmation email
        send_confirmation_email(email)
        flash("Signup successful! Please check your email to confirm your account.", "success")
        return render_template("home.html")

    # Confirm a token and decode the email
    def confirm_token(token, expiration=3600):
        serializer = URLSafeTimedSerializer(app.secret_key)
        try:
            email = serializer.loads(token, salt='email-confirmation-salt', max_age=expiration)
        except Exception:
            return False
        return email

    @app.route('/passReset/<token>', methods=['GET', 'POST'])
    def pass_reset(token):
        # Decode the token to extract the email
        email = confirm_token(token)
        if not email:
            flash("The confirmation link is invalid or has expired.", "danger")
            return render_template("home.html")

        # For GET request, render the page with modal
        return render_template("home.html", email=email, show_modal=True)

    @app.route('/confirm/<token>')
    def confirm_email(token):
        email = confirm_token(token)
        if not email:
            flash("The confirmation link is invalid or has expired.", "danger")
            return render_template("home.html")

        # Mark user as confirmed
        user = Users.query.filter_by(email=email).first()
        if user:
            user.is_confirmed = True
            db.session.commit()
            flash("Your email has been confirmed! You can now log in.", "success")
        else:
            flash("User not found.", "danger")
        return render_template("home.html")
    
    @app.route('/logout', methods=['POST'])
    def logout():
       session.pop('user_id', None)  # Remove user_id from session
       flash('You have been logged out.Visit us again. Thankyou!!', 'success')
       return render_template('home.html')

        
    @app.route('/reset-password', methods=['POST'])
    def resetPass():
        # Get the new password from the form
        email = request.form.get('email')
        new_password = request.form.get('newPassword')

        user = Users.query.filter_by(email=email).first()
        if user:
            # Update the user's password (hashed for security)
            user.password = new_password  # Store plain text password directly
            db.session.commit()
            flash("Your password has been updated successfully!", "success")
        else:
            flash("User not found.", "danger")
        return render_template("home.html")

    @app.route('/search', methods=['GET'])
    def search():
     query = request.args.get('query', '').lower()

     if any(keyword in query for keyword in ['earrings', 'ear', 'earing', 'earring','butti','buti']):
        earrings = Products.query.filter_by(category='earrings').all()
        return render_template('earrings.html', earrings=earrings)
     elif any(keyword in query for keyword in ['necklaces', 'neck', 'necklac', 'necklace','haar','har','set']):
        necklaces = Products.query.filter_by(category='necklace').all()
        return render_template('necklace.html', necklaces=necklaces)
     elif any(keyword in query for keyword in ['braceletes', 'bracelete', 'hand wear', 'hand','breslet','bracelet']):
        braceletes = Products.query.filter_by(category='bracelete').all()
        return render_template('bracelete.html', braceletes=braceletes)
     elif any(keyword in query for keyword in ['rings', 'ring', 'viti', 'finger','finger','rig']):
        rings = Products.query.filter_by(category='ring').all()
        return render_template('ring.html', rings=rings)
     else:
        return render_template('noMatches.html')


    return app
 
   