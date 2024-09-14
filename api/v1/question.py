""" Question endpoints """
from crypt import methods
from os import abort
from flask import Blueprint, request, jsonify, redirect, abort
from models.comment import Comment
from models.base import db
from models.base_redis import RedisServer
from models.question import Question
from models.tag import Tag
from models.user import User
from models.question_tag import QuestionTag
from models.vote import Vote
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


@question.route('/api/v1/questions/<int:id>', methods=['PUT'])
def update_question(id):
    """ endpoint used to update a question """
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

    question = db.session.query(Question).filter_by(id=id).first()
    if not question or not question.isActive:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({'Error': 'Invalid JSON data'}), 400
    title = data.get('title')
    if not title:
        return jsonify({'Error': 'Missing title'}), 400
    body = data.get('body')
    if not body:
        return jsonify({'Error': 'Missing body'}), 400

    question.title = title
    question.body = body
    question.updated_at = datetime.now(timezone.utc)
    db.session.commit()

    # removing all existing tags
    old_tags = db.session.query(QuestionTag).filter_by(
        question_id=question.id).all()
    for tag in old_tags:
        db.session.delete(tag)
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

    return jsonify({'message': 'Question updated'}), 200


@question.route('/api/v1/questions', methods=['GET'])
def get_questions():
    """ endpoint used to get all questions """
    questions = db.session.query(Question).order_by(
        Question.created_at.desc()).all()
    # convert to dictionary
    questions = [question.to_dict() for question in questions]
    # add number of comment for each question
    # and number of votes
    for question in questions:
        question['comments'] = db.session.query(Comment).filter_by(
            question_id=question['id']).count()
        votes = db.session.query(Vote).filter_by(
            parent_id=question['id'], parent_type='question').all()

        # count upvotes(isUpvote=True) and downvotes(isUpvote=False)
        question['upvotes'] = 0
        question['downvotes'] = 0
        for vote in votes:
            if vote.isUpvote:
                question['upvotes'] += 1
            else:
                question['downvotes'] += 1
    return jsonify(questions), 200
