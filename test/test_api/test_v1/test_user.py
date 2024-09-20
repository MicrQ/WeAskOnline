import unittest
from app import create_app, db 
from models.user import User
from werkzeug.security import generate_password_hash
from flask import json

class UserRoutesTestCase(unittest.TestCase):
    """Test case for user-related routes"""

    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        cls.app = create_app('testing')
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        """Set up a test user"""
        self.username = 'testuser'
        self.password = 'testpassword'
        self.hashed_password = generate_password_hash(self.password)
        self.user = User(username=self.username, password=self.hashed_password)
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        """Clean up after each test"""
        db.session.remove()
        db.drop_all()

    def test_register_success(self):
        """Test successful registration"""
        response = self.client.post('/api/v1/register', json={
            'username': 'newuser',
            'password': 'newpassword'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'User registered successfully', response.data)

    def test_register_fail_invalid_data(self):
        """Test registration with invalid data"""
        response = self.client.post('/api/v1/register', json={
            'username': 'newuser'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Username and password are required', response.data)

    def test_login_success(self):
        """Test successful login"""
        response = self.client.post('/api/v1/login', json={
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'token', response.data)

    def test_login_fail_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post('/api/v1/login', json={
            'username': self.username,
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Invalid username or password', response.data)

    def test_get_user_success(self):
        """Test get user details"""
        response = self.client.get(f'/api/v1/users/{self.user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'testuser', response.data)

    def test_get_user_fail_not_found(self):
        """Test get user details with non-existent user"""
        response = self.client.get('/api/v1/users/999')
        self.assertEqual(response.status_code, 404)

    def test_update_user_success(self):
        """Test successful user update"""
        token = self._generate_test_token()
        response = self.client.put(f'/api/v1/users/{self.user.id}', 
                                   json={'password': 'newpassword'}, 
                                   cookies={'api-token': token})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User updated successfully', response.data)

    def test_update_user_fail_unauthorized(self):
        """Test update user with invalid token"""
        response = self.client.put(f'/api/v1/users/{self.user.id}', 
                                   json={'password': 'newpassword'})
        self.assertEqual(response.status_code, 401)

    def test_delete_user_success(self):
        """Test successful user deletion"""
        token = self._generate_test_token()
        response = self.client.delete(f'/api/v1/users/{self.user.id}', 
                                      cookies={'api-token': token})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User deleted successfully', response.data)

    def test_delete_user_fail_unauthorized(self):
        """Test delete user with invalid token"""
        response = self.client.delete(f'/api/v1/users/{self.user.id}')
        self.assertEqual(response.status_code, 401)

    def _generate_test_token(self):
        """Generate a test token for user"""
        from werkzeug.security import generate_password_hash
        import jwt
        from datetime import datetime, timedelta

        SECRET_KEY = 'your_secret_key'
        TOKEN_EXPIRATION = 3600

        expiration = datetime.utcnow() + timedelta(seconds=TOKEN_EXPIRATION)
        payload = {
            'username': self.username,
            'exp': expiration
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token

if __name__ == '__main__':
    unittest.main()
