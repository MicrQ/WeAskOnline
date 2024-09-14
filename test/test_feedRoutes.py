#!/usr/bin/env python3
import unittest
from flask import Flask
from models.base import db
from models.feed import Feed
from models.base import Feed


class FeedRoutesTestCase(unittest.TestCase):
    """Tests for Feed routes"""

    @classmethod
    def setUpClass(cls):
        """Set up the Flask app and test client"""
        cls.app = Flask(__name__)
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        cls.app.register_blueprint(feed_routes)
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

    def test_create_feed_success(self):
        """Test successful feed creation"""
        response = self.client.post('/feeds', json={
            'content': 'This is a feed post',
            'user_id': 1
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Feed created successfully', response.json['message'])

    def test_create_feed_missing_fields(self):
        """Test feed creation with missing fields"""
        response = self.client.post('/feeds', json={
            'content': 'This is a feed post',
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing required fields', response.json['error'])


if __name__ == '__main__':
    unittest.main()
