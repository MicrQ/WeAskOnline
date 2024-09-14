""" Question endpoints """
from os import abort
from flask import Blueprint, request, jsonify, redirect, abort
from models.base import db
from models.base_redis import RedisServer
from models.question import Question
from models.tag import Tag
from models.user import User
from models.question_tag import QuestionTag
from datetime import datetime, timezone


question = Blueprint('question', __name__)


@question.route('/api/v1/questions', methods=['POST'])
def create_question():
    """ Handles question creation for logged in user """
    token = request.cookies.get('api-token')
    if not token:
        abort(401)

    redis = RedisServer()
    username = redis.get(token)
    if username is None:
        abort(401)
    user = db.session.query(User).filter_by(
        username=username.decode('utf-8')).first()
    if not user:
        abort(401)

    data = request.get_json()
    if not data:
        return jsonify({'Error': 'Invalid JSON data'}), 400
    title = data.get('title')
    if not title:
        return jsonify({'Error': 'Missing title'}), 400
    body = data.get('body')
    if not body:
        return jsonify({'Error': 'Missing body'}), 400

    now = datetime.now(timezone.utc)
    question = Question(
        title=title,
        body=body,
        user_id=user.id)
    db.session.add(question)
    db.session.commit()

    tags = data.get('tags')
    if tags:
        for tag in tags:
            tag_exists = db.session.query(Tag).filter_by(
                name=tag.lower()).first()
            new_tag = Tag(tag)
            if not tag_exists:
                db.session.add(new_tag)
                db.session.commit()
            new_tag = db.session.query(Tag).filter_by(
                name=new_tag.name).first()
            question_tag = QuestionTag(question.id, new_tag.id)
            db.session.add(question_tag)
            db.session.commit()

    return jsonify({'message': 'Question created'}), 201


# @question.route('api/v1/questions/<int:id>')
# def update_question(id):
#     """ endpoint used to  """
