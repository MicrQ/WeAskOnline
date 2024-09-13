import unittest
from app import create_app, db
from app.models import User

class UserRoutesTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app('testing')
        cls.client = cls.app.test_client()
        cls.ctx = cls.app.app_context()
        cls.ctx.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.ctx.pop()

    def test_get_user_me(self):
        response = self.client.get('/users/me')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'user details', response.data)
    def test_post_user(self):
        response = self.client.post('/users', json={'username': 'testuser', 'email': 'testuser@example.com'})
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'user created', response.data)

if __name__ == '__main__':
    unittest.main()
