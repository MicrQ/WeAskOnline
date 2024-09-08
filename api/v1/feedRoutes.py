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
    questions, comments, or any other relevant items for the feed.
    This fetches data from multiple tables such as Questions,
    Users, Comments, etc.

    Returns:
        JSON object with the feed data and HTTP 200 status.
    """
    # Fetch recent questions ( pulling the latest 10 questions)
    query = Question.query.order_by(desc(Question.created_at))
    recent_questions = query.limit(10).all()

    feed_data = []

    for question in recent_questions:
        # Retrieve user who posted the question
        user = User.query.filter_by(id=question.user_id).first()

        # Prepare question data for the feed
        question_data = {
            "question_id": str(question.id),
            "user": {
                "id": str(user.id),
                "username": "Sheldon",
                "firstname": "Godwin",
                "lastname": "Uwen",
            },
            "title": "Programming Language",
            "content": "I love python programming language?",
            "created_at": question.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "isActive": question.isActive
        }

        # Add question data to the feed
        feed_data.append(question_data)

    return jsonify({"feed": feed_data}), 200
