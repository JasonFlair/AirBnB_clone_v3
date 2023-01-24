#!/usr/bin/python3
""" Amenities Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref


class Amenity(BaseModel, Base):
    """the class for amenities"""
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    place_amenities = relationship("Place", secondary='place_amenity')
