#!/usr/bin/env python3
""" test for comment endpoints """
import unittest
from urllib import response
from app import app


class TestComment(unittest.TestCase):
    """ test for comments """
    def setUp(self):
        """ setting up necessary resources """
        self.app = app
        self.app.config['TESTING'] = True
        self.client = app.test_client()

    def test_post_comment(self):
        """ test to post a comment without being authorized """
        response = self.client.post('/api/v1/questions/1/comments', data={
            "body": "this is a test comment"
        })
        self.assertEqual(response.status_code, 401)

    def test_put_comment(self):
        """ test to update a comment without being authorized """
        response = self.client.put('/api/v1/questions/1/comments/1', data={
            "body": "this is a test comment"
        })
        self.assertEqual(response.status_code, 401)

    def test_delete_comment(self):
        """ test to delete comment without being authoried """
        response = self.client.delete('/api/v1/questions/1/comments/1')
        self.assertEqual(response.status_code, 401)
