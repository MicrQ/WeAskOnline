from flask import Blueprint
from api.v1.userRoutes import user_routes
from api.v1.questionRoutes import question_routes
from api.v1.tagRoutes import tag_routes
from api.v1.feedRoutes import feed_routes

home = Blueprint('home', __name__)

@home.route('/api/v1/')
def index():
    """\
    Root directory and first page for the developer to find
    moveable routes which route to find resources and to develop the frontend
    
    Returns:
        JSON List[Dict] - list of keys and values (hyperlinks) 
    """
    home_data = [
        {"message": "Hello, developer!"},
        {"login": "http://localhost:5000/api/v1/login"},
        {"register": "http://localhost:5000/api/register"},
        {"password_reset": "http://localhost:5000/api/password-reset"},
        {"user": "http://localhost:5000/api/users/<userid>"}
    ]
    return jsonify(home_data), 200
