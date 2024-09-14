#!/usr/bin/env python3
import unittest
from flask import Flask
from models.base import db
from models.tag import Tag
from api.v1.tag_routes import tag_routes


class TagRoutesTestCase(unittest.TestCase):
    """Tests for Tag routes"""

    @classmethod
    def setUpClass(cls):
        """Set up the Flask app and test client"""
        cls.app = Flask(__name__)
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        cls.app.register_blueprint(tag_routes)
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

    def test_create_tag_success(self):
        """Test successful tag creation"""
        response = self.client.post('/tags', json={
            'name': 'Tech'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Tag created successfully', response.json['message'])

    def test_create_tag_missing_fields(self):
        """Test tag creation with missing fields"""
        response = self.client.post('/tags', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Name is required', response.json['error'])


if __name__ == '__main__':
    unittest.main()
