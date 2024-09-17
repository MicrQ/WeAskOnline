#!/usr/bin/env python3
""" Module which stores the functionality of fetching tags from the DB """

from flask import Blueprint, abort, jsonify
from models.question_tag import QuestionTag
from models.base import db
from models.question import Question
from models.tag import Tag


tag = Blueprint('tag', __name__)


@tag.route('/api/v1/tags', methods=["GET"])
def get_tags():
    """ Return all Tags in a JSON format """
    tags = db.session.query(Tag).filter_by().all()
    if not tags:
        return jsonify(), 204
    all_tag = [tag.to_dict() for tag in tags]
    new_tag = []
    for tag in all_tag:
        print(tag.get("name"))
        tag['count'] = db.session.query(QuestionTag).filter_by(tag_id=tag['id']).count()
        new_tag.append(tag)
    return jsonify(new_tag), 200


@tag.route('/api/v1/tags/<string:name>')
def get_tags_with_name(name):
    """ Fetch questions with tag name passed to parameter
    passed on the route URL"""

    # Get the tag first and then search for the reoccurence of the tag
    # from the tag id
    tag = db.session.query(Tag).filter_by(name=name).first()
    if not tag:
        abort(404)
    
    # Get the id of the question_tag from the QuestionTag db and then search
    # for the question based on the found question tag id
    question_tag = db.session.query(QuestionTag).filter_by(tag_id=tag.id).first()
    if not question_tag:
        abort(404)
    
    # Get the question based on the id from the QuestionTag table
    questions = db.session.query(Question).filter_by(id=question_tag.question_id).all()
    if not questions:
        abort(404)
    
    # loop through the found questions to convert to serializable JSON data
    question_tag_data = []
    for question in questions:
        question_tag_data.append(question.to_dict())

    return jsonify(question_tag_data), 200
