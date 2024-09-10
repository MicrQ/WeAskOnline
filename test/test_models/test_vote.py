#!/usr/bin/env python3
""" test for Vote model """
from models.base import db
from models.reply import Reply
from models.comment import Comment
from models.question import Question
from models.user import User
from models.country import Country
from models.report import Report
from models.vote import Vote
from flask import Flask
import unittest
from sqlalchemy import text
from datetime import datetime, timezone


class testVoteModel(unittest.TestCase):
    """ test class for Vote model """

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

    def test_vote_creation(self):
        """ test fot creating a vote """
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
            title="What is python",
            body="I want someone to tell me what python is.",
            user_id=user.id,
            created_at=now,
            updated_at=now,
        )

        db.session.add(new_question)
        db.session.commit()

        question = db.session.query(Question).filter_by(created_at=now).first()
        self.assertIsNotNone(question)

        # creating comment properly
        new_comment = Comment(
            body="Python is a programming language.",
            created_at=now,
            user_id=user.id,
            question_id=question.id
        )

        db.session.add(new_comment)
        db.session.commit()

        comment = db.session.query(Comment).filter_by(created_at=now).first()
        self.assertIsNotNone(comment)

        new_reply = Reply(
            body="i know it is.",
            created_at=now,
            user_id=user.id,
            comment_id=comment.id
        )
        db.session.add(new_reply)
        db.session.commit()

        reply = db.session.query(Reply).filter_by(created_at=now).first()
        self.assertIsNotNone(reply)

        # voting reply properly
        new_vote = Vote(
            is_upvote=True,
            user_id=user.id,
            parent_type='reply',
            parent_id=reply.id
        )
        db.session.add(new_vote)
        db.session.commit()

        report = db.session.query(Vote).filter_by(
            parent_type='reply', parent_id=reply.id).first()
        self.assertIsNotNone(report)

        # voting comment properly
        new_vote = Vote(
            is_upvote=True,
            user_id=user.id,
            parent_type='comment',
            parent_id=comment.id
        )
        db.session.add(new_vote)
        db.session.commit()

        report = db.session.query(Vote).filter_by(
            parent_type='comment', parent_id=comment.id).first()
        self.assertIsNotNone(report)

        # voting question properly
        new_vote = Vote(
            is_upvote=True,
            user_id=user.id,
            parent_type='question',
            parent_id=question.id
        )
        db.session.add(new_vote)
        db.session.commit()

        report = db.session.query(Vote).filter_by(
            parent_type='question', parent_id=question.id).first()
        self.assertIsNotNone(report)


if __name__ == '__main__':
    unittest.main()
