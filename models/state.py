#!/usr/bin/python3
""" holds class State"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """Representation of state """
    __tablename__ = 'states'
    name = Column(String(128),
                  nullable=False)
    cities = relationship("City",
                          cascade="all, delete",
                          backref="states")

    def __init__(self, *args, **kwargs):
        """initializes state"""
        self.name = kwargs.pop("name", "")
        super().__init__(*args, **kwargs)

    @property
    def cities(self):
        """fs getter attribute that returns City instances"""
        values_city = models.storage.all("City").values()
        list_city = []
        for city in values_city:
            if city.state_id == self.id:
                list_city.append(city)
        return list_city
