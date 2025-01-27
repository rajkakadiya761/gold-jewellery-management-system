from flask import Blueprint, render_template, flash, request, redirect, url_for
from models import db, Users

# Create a Blueprint for manage users routes
manage_users_bp = Blueprint('manage_users', __name__)

@manage_users_bp.route('/manage-users', methods=['POST'])
def manageUsers():
    users = Users.query.all()
    return render_template('manageUsers.html', users=users)

@manage_users_bp.route('/addCustomer', methods=['POST'])
def add_customer():
    try:
        name = request.form['name']
        email = request.form['email']
        role = request.form['role']
        is_confirmed = request.form['is_confirmed']
        password = request.form['password']
        print("request.form:",request.form)

        new_user = Users(name=name,email=email,password=password, role=role,is_confirmed=is_confirmed)
        
        # Add to database session
        db.session.add(new_user)
        db.session.commit()  
        
        users = Users.query.all()
        flash('User added successfully!', 'success')
        return render_template('manageUsers.html', users=users)
    except Exception as e:
        db.session.rollback()
        return "Duplicate Entry Error or Technical Issue please try again"

@manage_users_bp.route('/update_customer/<int:user_id>', methods=['POST'])
def update_customer(user_id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        role = request.form['role']
        is_confirmed = request.form['is_confirmed']
        password = request.form['password']

        # Check if the email already exists for a different user
        existing_user = Users.query.filter(Users.email == email, Users.user_id != user_id).first()

        if existing_user:
            # Email already exists
            flash("Email already exists. Please use a different email.", "danger")
            users = Users.query.all()
            return render_template('manageUsers.html', users=users)

        # Find the user to update
        user = Users.query.get(user_id)
        # Update user details
        user.name = name
        user.email = email
        user.role = role
        user.password = password
        user.is_confirmed = is_confirmed

        # Save changes to the database
        db.session.commit()

        flash("User details updated successfully.", "success")
        users = Users.query.all()
        return render_template('manageUsers.html', users=users)

    return render_template("Accessing the page not supported via this navigation")

@manage_users_bp.route('/delete_customer/<int:user_id>', methods=['GET'])
def delete_customer(user_id):
    user = Users.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    users = Users.query.all()
    flash("User Deleted succesfully.", "success")
    return render_template('manageUsers.html', users=users)