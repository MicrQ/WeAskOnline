""" Question endpoints """
from crypt import methods
from os import abort
from flask import Blueprint, request, jsonify, redirect, abort, url_for
from models.comment import Comment
from models.base import db
from models.base_redis import RedisServer
from models.question import Question
from models.tag import Tag
from models.user import User
from models.question_tag import QuestionTag
from models.vote import Vote
from models.reply import Reply
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

    try:
        data = request.get_json()
    except Exception:
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

    if int(question.user_id) != user.id:
        return jsonify(
            {'Error': 'You don\'t have permission to delete this question'}
            ), 403

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
    questions = db.session.query(Question).filter_by(
        isActive=True).order_by(Question.created_at.desc()).all()
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
            if vote.is_upvote:
                question['upvotes'] += 1
            else:
                question['downvotes'] += 1
    return jsonify(questions), 200


@question.route('/api/v1/questions/<int:id>/<string:title>', methods=['GET'])
@question.route('/api/v1/questions/<int:id>', methods=['GET'])
def get_question(id, title=None):
    """ endpoint used to get a single question """
    question = db.session.query(Question).filter_by(id=id).first()
    if not question or not question.isActive:
        abort(404)

    # redirecting the user to the endpoint + title
    route_title = question.title.lower().replace(" ", "-").strip('?')
    if not title or title != route_title:
        return redirect(
            f'/api/v1/questions/{id}/{route_title}')

    question = question.to_dict()
    comments = db.session.query(Comment).filter_by(
        question_id=question['id']).all()
    question['comments'] = [comment.to_dict() for comment in comments]
    for comment in question['comments']:
        comment['upvotes'] = 0
        comment['downvotes'] = 0
        for vote in db.session.query(Vote).filter_by(parent_type='comment', parent_id=comment.get("id")).all():
            if vote.is_upvote:
                comment['upvotes'] += 1
            else:
                comment['downvotes'] += 1
        replies = db.session.query(Reply).filter_by(
            comment_id=comment['id']).all()
        comment['replies'] = [reply.to_dict() for reply in replies]

        for reply in comment['replies']:
            reply['upvotes'] = 0
            reply['downvotes'] = 0
            for reply in db.session.query(Vote).filter_by(parent_type='reply', parent_id=reply.get("id")).all():
                if reply.is_upvote:
                    reply['upvotes'] += 1
                else:
                    reply['downvotes'] += 1

    votes = db.session.query(Vote).filter_by(
        parent_id=question['id'], parent_type='question').all()

    # count upvotes(isUpvote=True) and downvotes(isUpvote=False)
    question['upvotes'] = 0
    question['downvotes'] = 0
    for vote in votes:
        if vote.is_upvote:
            question['upvotes'] += 1
        else:
            question['downvotes'] += 1
    return jsonify(question), 200


@question.route('/api/v1/questions/<int:id>', methods=['DELETE'])
def delete_question(id):
    """ route used to delete/deactivate a question """
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

    if int(question.user_id) != user.id:
        return jsonify(
            {'Error': 'You don\'t have permission to delete this question'}
            ), 403

    question.isActive = False
    db.session.commit()
    return jsonify({'message': 'Question deleted'}), 200


@question.route('/api/v1/questions/search', methods=['GET'])
def search_questions():
    """ route used to search questions """
    keyword = request.args.get('q')
    if not keyword:
        return redirect(url_for('question.get_questions'))

    questions = db.session.query(Question).filter(
        Question.title.ilike(f'%{keyword}%')).all()

    if not questions:
        abort(404)

    questions = [question.to_dict() for question in questions]

    return jsonify(questions), 200
