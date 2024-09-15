#!/usr/bin/env python3
""" Module for handling the comment logics C.R.U.D operations """
from flask import Blueprint, abort, jsonify, request

from models.base_redis import RedisServer
from models.comment import Comment
from models.question import Question
from models.base import db
from models.user import User


comment = Blueprint('comment', __name__)


@comment.route('/questions/<int:id>/comments/<int:comment_id', methods=['PUT'])
def update_comment(id, comment_id):
    """ Updates existing comment data """
    token = request.cookies.get('api-token')
    if not token:
        abort(401)

    redis = RedisServer()
    # Check if redis is connected to the database
    if not redis:
        return jsonify({'error': 'Redis is not running'}), 500

    username = redis.get(token)
    if not username:
        abort(401)

    data = request.get_json()
    updated_comment = data.get("body")

    if not data or updated_comment:
        return jsonify({'error': 'Comment body is empty'}), 400

    # Check if the question is a valid question in the database & check if
    # the comment is also valid in the database related to the question
    question = db.session.query(Question).filter_by(id=id).first()
    if not question:
        abort(404)

    comment = db.session.query(Comment).filter_by(user_id=comment_id).first()
    if not comment:
        abort(404)
    comment.body = updated_comment
    comment.isEdited = True
    db.session.commit()  
    return jsonify({'message': 'Success, comment updated.'}), 201


# DELETE - /questions/<id>/comments/<id>
@comment.route('/questions/<int:id>/comments/<int:comment_id>', methods="DELETE")
def delete_comment(id, comment_id):
    """ Deletes the comment based on the id of the comment and if the comment
    and if the comment is being posted by the owner of the comment """

    token = request.cookies.get('api-token')
    if not token:
        abort(401)

    redis = RedisServer()
    if not redis:
        return jsonify({'error': 'Redis is not running'}), 500
    username: str = redis.get(token)
    if not username:
        abort(401)
    try:
        user = db.session.query(User).filter_by(name=username.decode()).first()
        if not user:
            abort(401)
        question = db.session.query(Question).filter_by(id=id).first()
        if not question:
            abort(404)
        comment = db.session.query(Comment).filter_by(question_id=comment_id).first()
        if not comment:
            abort(404)
    except Exception as e:
        print("Error with fetching data from db: ", str(e))
        abort(404)
    
    # Check if the current user is the owner of the comment and have
    # access to delete the comment else abort 401
    if comment.id == user.id: 
        db.session.delete(comment)
        db.session.commit()
        return jsonify({'message': 'Success, comment deleted'}), 200
    else:
        abort(401)
