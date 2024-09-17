#!/usr/bin/env python3
""" test for question endpoints """
import unittest
from app import app


class TestQuestion(unittest.TestCase):
    """ testing questions endpoints """
    def setUp(self):
        """ setting up necessary resources """
        self.app = app
        self.app.config['TESTING'] = True
        self.client = app.test_client()

    def test_get_questions(self):
        """ test get questions """
        response = self.client.get('/api/v1/questions')
        self.assertEqual(response.status_code, 200)

    def test_get_question(self):
        """ test to get single question """
        response = self.client.get('/api/v1/questions/1')
        # check if this endpoit redirects to question/id/title
        self.assertEqual(response.status_code, 302)

    def test_post_question(self):
        """ test to post a question """
        response = self.client.post('/api/v1/questions', data={
            "title": "test question",
            "body": "this is a test question"
        })
        self.assertEqual(response.status_code, 401)

    def test_put_question(self):
        """ test to update a question """
        response = self.client.put('/api/v1/questions/1', data={
            "title": "test question",
            "body": "this is a test question"
        })
        self.assertEqual(response.status_code, 401)

    def test_delete_question(self):
        """ test to delete a question """
        response = self.client.delete('/api/v1/questions/1')
        self.assertEqual(response.status_code, 401)
