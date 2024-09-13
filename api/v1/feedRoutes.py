from flask import Blueprint, jsonify
from models import Question, User
from sqlalchemy import desc

# Define the blueprint for the feed routes
feed_routes = Blueprint('feed_routes', __name__)


# Get the feed for the user
@feed_routes.route('/feed', methods=['GET'])
def get_feed():
    """
    Handles retrieving the feed for the user which includes
    questions and user details for the feed.
    This fetches data from the Questions and Users tables.

    Returns:
        JSON object with the feed data and HTTP 200 status.
    """
    # Fetch recent questions (pulling the latest 10 questions)
    query = Question.query.order_by(desc(Question.created_at))
    recent_questions = query.limit(10).all()

    feed_data = []

    for question in recent_questions:
        # Retrieve user who posted the question
        user = User.query.get(question.user_id)
        
        # Check if user exists
        if user:
            user_data = {
                "id": str(user.id),
                "username": user.username,
                "firstname": user.firstname,
                "lastname": user.lastname
            }
        else:
            user_data = {
                "id": "Unknown",
                "username": "Unknown",
                "firstname": "Unknown",
                "lastname": "Unknown"
            }
        
        # Prepare question data for the feed
        question_data = {
            "question_id": str(question.id),
            "user": user_data,
            "title": question.title,
            "content": question.content,
            "created_at": question.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "isActive": question.isActive
        }

        # Add question data to the feed
        feed_data.append(question_data)

    return jsonify({"feed": feed_data}), 200
