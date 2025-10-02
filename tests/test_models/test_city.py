#!/usr/bin/python3
"""test for city"""
import unittest
import os
from models import city
from models.city import City
from models.base_model import BaseModel, Base
import pep8
import sqlalchemy


class TestCity(unittest.TestCase):
    """this will test the city class"""

    @classmethod
    def setUpClass(cls):
        """set up for test"""
        cls.city = City()
        cls.city.name = "LA"
        cls.city.state_id = "CA"

    @classmethod
    def teardown(cls):
        """at the end of the test this will tear it down"""
        del cls.city

    def tearDown(self):
        """teardown"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_City(self):
        """Tests pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/city.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_checking_for_docstring_City(self):
        """checking for docstrings"""
        self.assertIsNot(city.__doc__, None)
        self.assertIsNotNone(City.__doc__)

    def test_class_method_presence_City(self):
        """Test that the City methods are all present"""
        l1 = dir(City)
        self.assertIn('__init__', l1)
        self.assertIn('save', l1)
        self.assertIn('to_dict', l1)
        self.assertIn('__str__', l1)

    def test_class_attributes_City(self):
        """checking if City have attributes"""
        l1 = dir(City)
        self.assertIn('state_id', l1)
        self.assertIn('name', l1)

    def test_instance_attributes_City(self):
        """Test that the City instance attributes are all present"""
        l1 = dir(City())
        self.assertIn('id', l1)
        self.assertIn('updated_at', l1)
        self.assertIn('created_at', l1)
        self.assertIn('__class__', l1)
        self.assertIn('state_id', l1)
        self.assertIn('name', l1)

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != "db", "not a database")
    def test_class_attributes_City_db(self):
        """chekcing if City have DBStorage-related attributes"""
        l1 = dir(City)
        self.assertIn('__tablename__', l1)
        self.assertIn('places', l1)

    def test_is_subclass_City(self):
        """test if City is subclass of Basemodel"""
        self.assertTrue(issubclass(self.city.__class__, BaseModel), True)
        self.assertTrue(issubclass(self.city.__class__, Base), True)

    def test_attribute_types_City(self):
        """test attribute type for City"""
        self.assertEqual(type(self.city.name), str)
        self.assertEqual(type(self.city.state_id), str)

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != "db", "not a database")
    def test_attribute_types_City_db(self):
        """test attribute type for City"""
        self.assertEqual(type(self.city.__tablename__), str)
        self.assertEqual(type(self.city.places), sqlalchemy.orm.collections.
                         InstrumentedList)

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "skip test")
    def test_save_City(self):
        """test if the save works"""
        self.city.save()
        self.assertNotEqual(self.city.created_at, self.city.updated_at)

    def test_to_dict_City(self):
        """test if dictionary works"""
        self.assertEqual('to_dict' in dir(self.city), True)


if __name__ == "__main__":
    unittest.main()
