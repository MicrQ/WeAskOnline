#!/usr/bin/env python3
""" test for QuestionTag model """
from models.base import db
from models.tag import Tag
from models.question import Question
from models.question_tag import QuestionTag
from models.user import User
from models.country import Country
from flask import Flask
import unittest
from sqlalchemy import text
from datetime import datetime, timezone


class testQuestionTagModel(unittest.TestCase):
    """ test class for QuestionTag model """

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

    def test_create_question_tag(self):
        """ test creating new question tag model """
        new_country = Country(name='France')
        db.session.add(new_country)
        db.session.commit()

        country = db.session.query(Country).filter_by(name='France').first()
        self.assertIsNotNone(country)

        now = datetime.now(timezone.utc)
        new_User = User(
            firstname="John",
            lastname="Doe",
            bio="Software Engineer",
            username="johndoe",
            email="john@example.com",
            password="hashed_password",
            created_at=now,
            updated_at=now,
            country_id=country.id
        )

        db.session.add(new_User)
        db.session.commit()

        user = db.session.query(User).filter_by(username='johndoe').first()
        self.assertIsNotNone(user)

        new_question = Question(
            title = "What is python",
            body = "I want someone to tell me what python is.",
            user_id = user.id,
            created_at = now,
            updated_at = now,
        )

        db.session.add(new_question)
        db.session.commit()

        question = db.session.query(Question).filter_by(created_at=now).first()
        self.assertIsNotNone(question)

        new_tag = Tag(name='python')
        db.session.add(new_tag)
        db.session.commit()
        tag = db.session.query(Tag).filter_by(name='python').first()
        self.assertIsNotNone(tag)

        new_question_tag = QuestionTag(question_id=question.id, tag_id=tag.id)
        db.session.add(new_question_tag)
        db.session.commit()
        question_tag = db.session.query(QuestionTag).filter_by(question_id=question.id).first()
        self.assertIsNotNone(question_tag)

        # test with invalid tag id
        new_question_tag = QuestionTag(question_id=question.id, tag_id=-1)
        with self.assertRaises(Exception):
            db.session.add(new_question_tag)
            db.session.commit()
        db.session.rollback()

        # test with invalid question id
        new_question_tag = QuestionTag(question_id=-1, tag_id=tag.id)
        with self.assertRaises(Exception):
            db.session.add(new_question_tag)
            db.session.commit()


if __name__ == '__main__':
    unittest.main()
