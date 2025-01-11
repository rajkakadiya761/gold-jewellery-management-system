from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'this_is_my_secret_key'  # Session storage needs this
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/arihant'  # Replace password if applicable
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
db = SQLAlchemy(app)  # ORM setup

class Users(db.Model):
    __tablename__ = 'users'  # Explicitly setting the table name to 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)

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
    if user and user.password == password and user.role=="Customer":
        flash("User Login Successful!", "success")  # Flash success message
    elif user and user.password == password and user.role=="Admin":
        flash("Admin Login Successful!", "success")  # Flash success message
        return render_template("admin.html")
    else:
        flash("Login Failed! Invalid email or password.", "danger")  # Flash error message
    
    return render_template("home.html")  # Stay on the same page and display the flash message

@app.route('/signup', methods=['POST'])
def signUp():
    # Retrieve form data
    name = request.form['signupName']
    email = request.form['signupEmail']
    password = request.form['signupPassword']

    # Check if the email already exists in the database
    existing_user = Users.query.filter_by(email=email).first()
    if existing_user:
        flash("Email already exists. Please use a different email.", "danger")
    else:
        # Create a new user and add it to the database
        new_user = Users(name=name, email=email, password=password, role="Customer")
        db.session.add(new_user)
        db.session.commit()

        # Flash success message and redirect
        flash("Signup successful! You can now log in.", "success")
    return render_template("home.html")
    

if __name__ == "__main__":
    app.run(debug=True)
