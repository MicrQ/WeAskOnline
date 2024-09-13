#!/usr/bin/env python3
""" test for role model """
from models.base import db
from models.role import Role
from flask import Flask
import unittest


class testRoleModel(unittest.TestCase):
    """ test class for Role model """

    def setUp(self):
        """ setup the in memory db and create the table """
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.app_context().push()

        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        """ teardown the db and drop the table """
        db.session.remove()
        db.drop_all()

    def test_role_creation(self):
        """ test creating new role """
        new_role = Role(name="Admin")
        db.session.add(new_role)
        db.session.commit()

        role = Role.query.filter_by(name="Admin").first()
        self.assertIsNotNone(role)
        self.assertEqual(role.name, "Admin")

        duplicate_role = Role(name="Admin")
        db.session.add(duplicate_role)
        with self.assertRaises(Exception):
            db.session.commit()


if __name__ == '__main__':
    unittest.main()
