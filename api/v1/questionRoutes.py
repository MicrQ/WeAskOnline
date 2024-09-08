from flask import Blueprint, jsonify, request
from models import Question, User, db

question_routes = Blueprint('question_routes', __name__)


# Route: Get all questions
@question_routes.route('/questions', methods=['GET'])
def get_all_questions():
    questions = Question.query.all()
    questions_data = [
        {
            "id": str(question.id),
            "user_id": str(question.user_id),
            "title": question.title,
            "content": question.content,
            "created_at": question.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": question.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            "isActive": question.isActive
        } for question in questions
    ]
    return jsonify({"questions": questions_data}), 200


# Route: Get specific question by ID
@question_routes.route('/questions/<uuid:id>', methods=['GET'])
def get_question_by_id(id):
    question = Question.query.get(id)
    if question:
        user = User.query.get(question.user_id)
        question_data = {
            "id": str(question.id),
            "user": {
                "id": str(user.id),
                "username": user.username
            },
            "title": question.title,
            "content": question.content,
            "created_at": question.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": question.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            "isActive": question.isActive
        }
        return jsonify({"question": question_data}), 200
    return jsonify({"error": "Question not found"}), 404


# Route: Create a new question
@question_routes.route('/questions', methods=['POST'])
def create_question():
    data = request.get_json()
    question = Question(**data)
    db.session.add(question)
    db.session.commit()
    return jsonify({"message": "Question created", "data": data}), 201


# Route: Delete a question
@question_routes.route('/questions/<uuid:id>/delete', methods=['DELETE'])
def delete_question(id):
    question = Question.query.get(id)
    if question:
        db.session.delete(question)
        db.session.commit()
        return jsonify({"message": f"Question {id} deleted"}), 200
    return jsonify({"error": "Question not found"}), 404
