#!/usr/bin/env python3
""" test for tag model """
from models.base import db
from models.tag import Tag
from flask import Flask
import unittest
from sqlalchemy import text


class testTagModel(unittest.TestCase):
    """ test class for Tag model """

    def setUp(self):
        """ setup the in memory db and create the table """
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.app_context().push()

        db.init_app(self.app)
        with self.app.app_context():
            db.session.execute(text('PRAGMA foreign_keys = ON'))
            db.create_all()

    def tearDown(self):
        """ teardown the db and drop the table """
        db.session.remove()
        db.drop_all()

    def test_create_tag(self):
        """ test creating new tag model """
        new_tag = Tag(name='Python')
        db.session.add(new_tag)
        db.session.commit()

        tag = db.session.query(Tag).filter_by(name='Python').first()
        self.assertIsNone(tag)

        tag = db.session.query(Tag).filter_by(name='python').first()
        self.assertIsNotNone(tag)

        # test duplicate tag
        db.session.add(Tag(name='python'))
        with self.assertRaises(Exception):
            db.session.commit()


if __name__ == "__main__":
    unittest.main()
