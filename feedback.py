from flask import Blueprint, render_template, flash, request, redirect, url_for, session, jsonify
from models import db, Feedback, Users
from datetime import datetime

manage_feedbacks = Blueprint('Feedback', __name__)

@manage_feedbacks.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    print("User session:", session.get('user_id'))  # Debug log
    if 'user_id' not in session:
        return jsonify({'error': 'You must be logged in to submit feedback'}), 403

    data = request.json
    rating = data.get('rating')
    message = data.get('message')
    product_id = data.get('product_id')

    # Validate inputs
    if not all([rating, message, product_id]):
        print("Missing required fields:", data)  # Debug log
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            return jsonify({'error': 'Invalid rating'}), 400
    except ValueError:
        return jsonify({'error': 'Rating must be a number'}), 400

    # Create a new feedback entry
    feedback = Feedback(
        user_id=session['user_id'],  # Fetch logged-in user ID
        product_id=product_id,
        ratings=rating,
        message=message,
        feedback_date=datetime.now()
    )

    # Store feedback in the database
    try:
        db.session.add(feedback)
        db.session.commit()
        print(f"Feedback saved: {feedback}")  # Debug log
        return jsonify({'message': 'Feedback submitted successfully', 'status': 'success'})
    except Exception as e:
        print(f"Error saving feedback: {e}")  # Debug log
        db.session.rollback()  # Ensure the session is rolled back if any error occurs
        return jsonify({'error': 'Failed to submit feedback'}), 500



@manage_feedbacks.route('/get_feedbacks/<int:product_id>', methods=['GET'])
def get_feedbacks(product_id):
    feedbacks = (
        db.session.query(Feedback, Users.email)
        .join(Users, Feedback.user_id == Users.user_id)  # Join Feedback with Users table
        .filter(Feedback.product_id == product_id)
        .all()
    )

    feedback_list = [
        {
            "email": user_email,  # Fetch email instead of customer name
            "ratings": feedback.ratings,
            "message": feedback.message,
            "feedback_date": feedback.feedback_date.strftime("%Y-%m-%d")
        }
        for feedback, user_email in feedbacks
    ]

    return jsonify(feedback_list)

@manage_feedbacks.route('/manage-feedback', methods=['POST'])
def manage_feedback():
    feedbacks = Feedback.query.all()  # Fetch all feedback entries

    feedback_data = []
    for feedback in feedbacks:
        feedback_data.append({
            "feedback_id": feedback.feedback_id,
            "user_id": feedback.user.user_id if feedback.user else "Unable to fetch",
            "user_name": feedback.user.name if feedback.user else "Unknown User",
            "Email": feedback.user.email if feedback.user else "Unknown User",
            "product_id": feedback.product.product_id if feedback.product else "Unable to fetch",
            "product_name": feedback.product.name if feedback.product else "Unknown Product",
            "ratings": feedback.ratings,
            "message": feedback.message,
            "feedback_date": feedback.feedback_date.strftime("%Y-%m-%d")
        })

    return render_template(
        'viewFeedback.html',
        feedbacks=feedback_data
    )
