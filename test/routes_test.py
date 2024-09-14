#!/usr/bin/env python3
import unittest
from flask import Flask
from models.base import db
from api.v1.routes import main_routes
from models.user import User


class MainRoutesTestCase(unittest.TestCase):
    """Tests for general routes"""

    @classmethod
    def setUpClass(cls):
        """Set up the Flask app and test client"""
        cls.app = Flask(__name__)
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        cls.app.register_blueprint(main_routes)
        cls.client = cls.app.test_client()
        cls.app.app_context().push()
        db.init_app(cls.app)
        with cls.app.app_context():
            db.session.execute('PRAGMA foreign_keys = ON')
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Tear down the test database"""
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_example_route_success(self):
        """Test an example route"""
        response = self.client.get('/example')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Example response', response.json['message'])

    def test_example_route_error(self):
        """Test error handling in an example route"""
        response = self.client.get('/example-error')
        self.assertEqual(response.status_code, 500)
        self.assertIn('Internal Server Error', response.json['error'])


if __name__ == '__main__':
    unittest.main()
