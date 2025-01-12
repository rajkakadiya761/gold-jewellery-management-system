from flask import Flask, render_template, request, jsonify, flash, url_for
from markupsafe import Markup
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
app.secret_key = 'this_is_my_secret_key'  # Session storage needs this
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/arihant'  # Replace password if applicable
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Replace with your mail server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'krisha4801@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'khmg oflh ddyq oxey'  # Replace with your email password

db = SQLAlchemy(app)  # ORM setup
mail = Mail(app)  # Email setup

class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_confirmed = db.Column(db.Integer, default=0)  # Add confirmation status

    def __repr__(self):
        return f"<User {self.name}, {self.email}>"

# Route for Home Page
@app.route("/")
def page1():
    return render_template("home.html")

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
                flash("User Login Successful!", "success")  # Flash success message
            elif user and user.password == password and user.role=="Admin":
                flash("Admin Login Successful!", "success")  # Flash success message
                return render_template("admin.html")
        else:
            link = Markup(
                'Please confirm Email Verification Link! '
                '<a href="{}">Click here</a> if you want the link to be re-sent.'.format(url_for('resend_confirmation', email=email))
            )
            flash(link, "danger")
    else:
        flash("Login Failed! Invalid email or password.", "danger")  # Flash error message
    
    return render_template("home.html")  # Stay on the same page and display the flash message

@app.route('/resend-confirmation')
def resend_confirmation():
    email = request.args.get('email')
    if email:
        send_confirmation_email(email)
        flash("Verification email has been re-sent.", "success")
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
    

if __name__ == "__main__":
    app.run(debug=True)
