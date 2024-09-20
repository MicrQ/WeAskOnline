#!/usr/bin/python3
""" test for authentication """
import unittest
from urllib import response
from app import app


class TestAuth(unittest.TestCase):
    """ test authentication """
    def setUp(self):
        """ setting up the necessary things """
        self.app = app
        self.app.config['TESTING'] = True
        self.client = app.test_client()

    def test_logout(self):
        """ test logout operation """
        response = self.client.get('/api/v1/logout')
        # self.assertEqual(response.status_code, 204)

    def test_login_with_no_data(self):
        """ testing login """
        response = self.client.post('/api/v1/login')
        self.assertEqual(response.status_code, 400)

    def test_login_with_either_username_password_only(self):
        """ test only sending one of the fields for the form data """
        response = self.client.post('/api/v1/login', data={
            "username": "test"
        })
        self.assertEqual(response.status_code, 400)
        # checking if the returned message is Missing password
        self.assertIn(b"Missing password", response.data)

        response = self.client.post('/api/v1/login', data={"password": "test"})
        self.assertEqual(response.status_code, 400)
        # checking if the returned message is Missing password
        self.assertIn(b"Missing username", response.data)

    def test_login_with_invalid_credentials(self):
        """ test login with invalid credentials """
        response = self.client.post('/api/v1/login', data={
            "username": "test",
            "password": "test"
        })
        self.assertEqual(response.status_code, 401)
        # checking if the returned message is Invalid username
        self.assertIn(b"Invalid username", response.data)
