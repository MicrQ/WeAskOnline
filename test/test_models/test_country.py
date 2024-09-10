#!/usr/bin/env python3
""" test for country model """
from models.base import db
from models.country import Country
from flask import Flask
import unittest


class testCountryModel(unittest.TestCase):
    """ test class for Country model """

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

    def test_country_creation(self):
        """ test creating new country """
        new_country = Country(name="France")
        db.session.add(new_country)
        db.session.commit()

        country = Country.query.filter_by(name="France").first()
        self.assertIsNotNone(country)
        self.assertEqual(country.name, "France")

        duplicate_country = Country(name="France")
        db.session.add(duplicate_country)
        with self.assertRaises(Exception):
            db.session.commit()


if __name__ == '__main__':
    unittest.main()
