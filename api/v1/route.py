from flask import Blueprint
from api.V1.userRoutes import user_routes
from api.V1.questionRoutes import question_routes
from api.V1.tagRoutes import tag_routes
from api.V1.feedRoutes import feed_routes

# Initialize blueprint
api_v1 = Blueprint('api_v1', __name__)

# Register all routes
api_v1.register_blueprint(user_routes, url_prefix='/users')
api_v1.register_blueprint(question_routes, url_prefix='/questions')
api_v1.register_blueprint(tag_routes, url_prefix='/tags')
api_v1.register_blueprint(feed_routes, url_prefix='/feed')
