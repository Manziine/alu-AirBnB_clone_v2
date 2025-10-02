#!/usr/bin/python3
"""test for state"""
import unittest
import os
from models import state
from models.state import State
from models.base_model import BaseModel, Base
import pep8
import sqlalchemy


class TestState(unittest.TestCase):
    """this will test the State class"""

    @classmethod
    def setUpClass(cls):
        """set up for test"""
        cls.state = State()
        cls.state.name = "CA"

    @classmethod
    def teardown(cls):
        """at the end of the test this will tear it down"""
        del cls.state

    def tearDown(self):
        """teardown"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_Review(self):
        """Tests pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/state.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_checking_for_docstring_State(self):
        """checking for docstrings"""
        self.assertIsNotNone(state.__doc__)
        self.assertIsNotNone(State.__doc__)

    def test_class_method_presence_State(self):
        """Test that the State instance has the same methods"""
        l1 = dir(State)
        self.assertIn('__init__', l1)
        self.assertIn('save', l1)
        self.assertIn('to_dict', l1)
        self.assertIn('__str__', l1)

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "not a database")
    def test_instance_method_presence_State_additional(self):
        """Test that the State instance has the extra "cities" method"""
        l1 = dir(State())
        self.assertIn('cities', l1)

    def test_class_attribute_presence_State(self):
        """Test that the State attributes are all present"""
        l1 = dir(State)
        self.assertIn('name', l1)

    def test_instance_attribute_presence(self):
        """Test that the State instance attributes are all present"""
        l1 = dir(State())
        self.assertIn('id', l1)
        self.assertIn('updated_at', l1)
        self.assertIn('created_at', l1)
        self.assertIn('__class__', l1)
        self.assertIn('name', l1)

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != "db", "not a database")
    def test_class_attributes_State_db(self):
        """chekcing if State have DBStorage-related attributes"""
        l1 = dir(State)
        self.assertIn('__tablename__', l1)
        self.assertIn('cities', l1)

    def test_is_subclass_State(self):
        """test if State is subclass of BaseModel"""
        self.assertTrue(issubclass(self.state.__class__, BaseModel), True)
        self.assertTrue(issubclass(self.state.__class__, Base), True)

    def test_attribute_types_State(self):
        """test attribute type for State"""
        self.assertEqual(type(self.state.name), str)

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != "db", "not a database")
    def test_attribute_types_State_db(self):
        """test attribute type for State"""
        self.assertEqual(type(self.state.__tablename__), str)
        self.assertEqual(type(self.state.cities), sqlalchemy.orm.collections.
                         InstrumentedList)

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "skip test")
    def test_save_State(self):
        """test if the save works"""
        self.state.save()
        self.assertNotEqual(self.state.created_at, self.state.updated_at)

    def test_to_dict_State(self):
        """test if dictionary works"""
        self.assertEqual('to_dict' in dir(self.state), True)


if __name__ == "__main__":
    unittest.main()
