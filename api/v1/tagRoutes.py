from flask import Blueprint, jsonify
from models import db  # Assuming SQLAlchemy models and instance

tag_routes = Blueprint('tag_routes', __name__)


# Route: Get all tags
@tag_routes.route('/question/tags', methods=['GET'])
def get_tags():
    # Replace this with actual tag fetching logic
    tags = []  # Fetch tags from the database
    return jsonify({"tags": tags}), 200
