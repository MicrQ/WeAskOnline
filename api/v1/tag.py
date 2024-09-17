#!/usr/bin/env python3
""" Module which stores the functionality of fetching tags from the DB """

from flask import Blueprint, jsonify
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
