# -*- encoding: utf-8 -*-

"""
Base Class for Database Schemas uses Declarative Base
"""

from sqlalchemy.orm import DeclarativeBase

class BaseSchema(DeclarativeBase):
    """
    Shared Declarative Base for all APTracker ORM Models
    """

    pass
