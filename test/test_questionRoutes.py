import unittest
from app import create_app, db
from app.models import Question
from app import create_app, db


class QuestionRoutesTestCase(unittest.TestCase):
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

    def test_get_questions(self):
        response = self.client.get('/questions')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'questions', response.data)

    def test_post_question(self):
        response = self.client.post(
            '/questions', json={'title': 'Test Question',
                                'body': 'This is a test question.'
                                })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'question created', response.data)

    def test_post_question_invalid(self):
        response = self.client.post('/questions',
                                    json={'title': '', 'body': ''
                                          })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid input', response.data)


if __name__ == '__main__':
    unittest.main()
