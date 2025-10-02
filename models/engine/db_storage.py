#!/usr/bin/python3
"""This is the file storage class for AirBnB"""
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv


class DBStorage:
    """This class stores data to the MySQL database
    Attributes:
        __engine: None
        __session: None
    """
    __engine = None
    __session = None
    all_classes = {"State", "City", "User", "Amenity", "Place", "Review"}

    def __init__(self):
        """create the engine and links it to the MySQL database and user"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(getenv('HBNB_MYSQL_USER'),
                                             getenv('HBNB_MYSQL_PWD'),
                                             getenv('HBNB_MYSQL_HOST'),
                                             getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """returns a dictionary of instances/objects
        Return:
            returns a dictionary like FileStorage (__objects)
        """
        if cls:
            try:
                return {'{}.{}'.format(type(obj).__name__, obj.id): obj
                        for obj in self.__session.query(eval(cls)).all()
                        if eval(cls).__name__ == type(obj).__name__}
            except:
                return {}
        else:
            obj_list = []
            for cls_name in self.all_classes:
                for obj in self.__session.query(eval(cls_name)).all():
                    obj_list.append(obj)
            return {'{}.{}'.format(type(obj).__name__, obj.id): obj
                    for obj in obj_list}

    def new(self, obj):
        """add the object to the current database session
        Args:
            obj: given object
        """
        if obj:
            self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session
        """
        self.__session.commit()

    def reload(self):
        """create all tables in the database
        and create the current database session
        """
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Scoped_Session = scoped_session(Session)
        self.__session = Scoped_Session()

    def delete(self, obj=None):
        """delete obj from the current database session
        """
        if obj:
            self.__session.delete(obj)
        self.save()

#    Note: leave this here, might use later?
#    Not sure why we are NOT being asked to close the sessions
#    In Project 0x0F, I always closed sessions prior to terminating
#    That is a question we should ask
#
    def close(self):
        """close the current database session
        """
        self.__session.close()
