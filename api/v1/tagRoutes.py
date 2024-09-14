from flask import Blueprint, jsonify
from models import Tag, db
tag_routes = Blueprint('tag_routes', __name__)


#  Get all tags
@tag_routes.route('/question/tags', methods=['GET'])
def get_tags():
    try:
        # Query the database to get all tags
        tags = Tag.query.all()

        # Format the tag data to be returned as a JSON response
        tag_list = [{"id": tag.id, "name": tag.name} for tag in tags]

        return jsonify({"tags": tag_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
