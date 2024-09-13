import unittest
from app import create_app, db
from app.models import Tag

class TagRoutesTestCase(unittest.TestCase):
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

    def test_get_tags(self):
        response = self.client.get('/tags')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        # Adjust the assertion based on the actual structure of your response
        self.assertIn('tags', data)

    def test_post_tag(self):
        response = self.client.post('/tags', json={'name': 'Test Tag'})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        # Adjust the assertion based on the actual structure of your response
        self.assertEqual(data['message'], 'tag created')

if __name__ == '__main__':
    unittest.main()
