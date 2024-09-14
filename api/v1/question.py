#!/usr/bin/env python3

from flask import Blueprint, jsonify
from models.base import db
from models.comment import Comment
from models.question import Question


question = Blueprint("question", __name__)

@question.route('/api/v1/questions', methods=["GET"])
def get_question():
    """Render all the recent questions stored in the database as a feed"""
    all_question = db.session.query(Question, Comment).join(
      Comment, Comment.question_id == Question.id, 
      isouter=True).order_by(Question.created_at)

    data = []
    for question in all_question:
        data.append(question)
    
    return jsonify(data), 200


@question.route('/api/v1/questions/<question_id>', methods=["GET"])
def get_question(question_id):
    """Retrieve only sepcific Question from the database based on the
    Question.id
    """
    try:
        question = db.session.query(Question).filter(id = question_id).first()
        return jsonify(question), 200
    except Exception:
        print(Exception)
