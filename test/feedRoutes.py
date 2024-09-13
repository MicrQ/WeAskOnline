import unittest
from app import create_app, db
from app.models import Feed

class FeedRoutesTestCase(unittest.TestCase):
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

    def test_get_feeds(self):
        response = self.client.get('/feeds')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'feeds', response.data)
    def test_post_feed(self):
        response = self.client.post('/feeds', json={'title': 'Test Feed', 'content': 'This is a test feed.'})
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'feed created', response.data)
    def test_post_feed_invalid(self):
        response = self.client.post('/feeds', json={'title': '', 'content': ''})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid input', response.data)

if __name__ == '__main__':
    unittest.main()
