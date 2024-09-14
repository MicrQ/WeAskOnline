#!/usr/bin/env python3
import unittest
from flask import Flask
from models.base import db
from models.user import User
# from api.v1.user_routes import user_routes
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash


class UserRoutesTestCase(unittest.TestCase):
    """Tests for User routes"""

    @classmethod
    def setUpClass(cls):
        """Set up the Flask app and test client"""
        cls.app = Flask(__name__)
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        cls.app.register_blueprint(user_routes)
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

    def test_create_user_success(self):
        """Test successful user creation"""
        response = self.client.post('/users', json={
            'firstname': 'John',
            'lastname': 'Doe',
            'username': 'johndoe',
            'email': 'john@example.com',
            'password': 'securepassword'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('User created successfully', response.json['message'])

    def test_create_user_missing_fields(self):
        """Test user creation with missing fields"""
        response = self.client.post('/users', json={
            'firstname': 'John',
            'lastname': 'Doe',
            'username': 'johndoe',
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing required fields', response.json['error'])

    def test_create_user_existing_email(self):
        """Test user creation with existing email"""
        self.client.post('/users', json={
            'firstname': 'John',
            'lastname': 'Doe',
            'username': 'johndoe',
            'email': 'john@example.com',
            'password': 'securepassword'
        })
        response = self.client.post('/users', json={
            'firstname': 'Jane',
            'lastname': 'Smith',
            'username': 'janesmith',
            'email': 'john@example.com',
            'password': 'anotherpassword'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Email already exists', response.json['error'])

    def test_create_user_existing_username(self):
        """Test user creation with existing username"""
        self.client.post('/users', json={
            'firstname': 'John',
            'lastname': 'Doe',
            'username': 'johndoe',
            'email': 'john@example.com',
            'password': 'securepassword'
        })
        response = self.client.post('/users', json={
            'firstname': 'Jane',
            'lastname': 'Smith',
            'username': 'johndoe',
            'email': 'jane@example.com',
            'password': 'anotherpassword'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Username already exists', response.json['error'])

    def test_get_user_success(self):
        """Test retrieving a user by ID"""
        response = self.client.post('/users', json={
            'firstname': 'John',
            'lastname': 'Doe',
            'username': 'johndoe',
            'email': 'john@example.com',
            'password': 'securepassword'
        })
        user_id = response.json['id']
        response = self.client.get(f'/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('johndoe', response.json['username'])

    def test_get_user_not_found(self):
        """Test retrieving a user with non-existent ID"""
        response = self.client.get('/users/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('User not found', response.json['error'])


if __name__ == '__main__':
    unittest.main()
