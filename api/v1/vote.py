#!/usr/bin/env python3
""" Handles the voting system """

from flask import Blueprint, abort, jsonify, request
from models.base_redis import RedisServer
from models.comment import Comment
from models.question import Question
from models.reply import Reply
from models.base import db
from models.user import User
from models.vote import Vote


vote = Blueprint('vote', __name__)


@vote.route('/api/v1/vote/<string:entity>/<int:id>', methods=['POST'])
def create_vote(entity, id):
    """ Add vote to a db based on the response for the JSON data sent """
    token = request.cookies.get('api-token')
    if not token:
        abort(401)

    redis = RedisServer()
    if not redis:
        return jsonify({'error': 'Redis server is not running'}), 500
    
    username = redis.get(token)
    if not username:
        abort(401)
    user = db.session.query(User).filter_by(username=username.decode('UTF-8')).first()
    if not user:
        abort(401)

    entities = {
        'comment': Comment,
        'question': Question,
        'reply': Reply
        }
    if entity.lower() not in entities.keys():
        abort(404)
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Empty body found'}), 400
    
    vote = data.get('vote')
    if not vote:
        return jsonify({'error': 'Missing vote entity'}), 400

    vote = vote.lower()

    model = db.session.query(entities.get(entity)).filter_by(id=id).first()
    if not model:
        abort(404)
    
    check_user_vote = db.session.query(Vote).filter_by(
        parent_type=entity.lower(),
        parent_id=id,
        user_id=user.id
        ).first()

    if not check_user_vote:
        if vote not in ["novote", "upvote", "downvote"]:
            return jsonify({'error': 'Invalid vote entity'}), 400

        user_vote = Vote(
            is_upvote=False,
            user_id=user.id, parent_type=entity.lower(),
            parent_id=id)
        
        # db.session.add(user_vote)

        if vote == 'upvote':
            user_vote.is_upvote = True
        db.session.add(user_vote)

    elif check_user_vote:
        if vote == 'novote':
            db.session.delete(check_user_vote)
        elif vote == 'downvote':
            check_user_vote.is_upvote = False
        elif vote == 'upvote':
            check_user_vote.is_upvote = True
        else:
            db.session.close()
            return jsonify({'error': 'Invalid vote entity'}), 400

    db.session.commit()
    return jsonify({'message': 'Success'}), 200
