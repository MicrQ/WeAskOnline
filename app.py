from flask import Flask
from api.v1.auth import auth


app = Flask(__name__)
app.register_blueprint(auth)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
