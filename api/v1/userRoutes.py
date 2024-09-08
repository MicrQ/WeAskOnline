from flask import Blueprint, jsonify, request
from models import User, db  # Assuming SQLAlchemy models and instance

user_routes = Blueprint('user_routes', __name__)

# Route: User Dashboard
@user_routes.route('/dashboard', methods=['GET'])
def dashboard():
    return jsonify({"message": "User dashboard"}), 200

# Route: Get current user details
@user_routes.route('/users/me', methods=['GET'])
def get_current_user():
    # Assuming you have a way to get the current user (e.g., from a token)
    user_id = request.args.get('user_id')  # Replace with actual user identification method
    user = User.query.get(user_id)
    if user:
        user_data = {
            "id": str(user.id),
            "firstname": user.firstname,
            "lastname": user.lastname,
            "username": user.username,
            "email": user.email,
            "bio": user.bio,
            "country_id": user.country_id,
            "profile_image": user.profile_image,
            "created_at": user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": user.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            "isActive": user.isActive
        }
        return jsonify({"user": user_data}), 200
    return jsonify({"error": "User not found"}), 404

# Route: Update user by ID
@user_routes.route('/users/<uuid:user_id>', methods=['POST'])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    if user:
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        db.session.commit()
        return jsonify({"message": f"User {user_id} updated", "data": data}), 200
    return jsonify({"error": "User not found"}), 404

# Route: Delete user account
@user_routes.route('/users/<uuid:user_id>/delete_account', methods=['POST'])
def delete_user_account(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"User {user_id} account deleted"}), 200
    return jsonify({"error": "User not found"}), 404
