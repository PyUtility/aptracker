# -*- encoding: utf-8 -*-

"""
SQL Alchemy ORM Schema Definitions for APTracker

Declares relational database tables that backs the :mod:`APTracker`
persistence layer using :mod:`SQLAlchemy` ORM framework. All objects
(tables, functions, etc.) are prefixed with ``apt_`` to avoid name
collision when the module shares the database with other application.
"""

import datetime as dt

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, String, DateTime, Index, ForeignKey

from aptracker._base.schema import BaseSchema

class ProjectRecord(BaseSchema):
    """
    ORM Mapping for the ``apt_project`` Table in a Relational DB
    """

    __tablename__ = "apt_project"

    job_name : Mapped[str] = Column(String(36), primary_key = True)
    job_description : Mapped[str] = Column(
        String(128), unique = True, nullable = False
    )

    created_on : Mapped[dt.datetime] = Column(
        DateTime(timezone = True), nullable = False,
        default = dt.datetime.now()
    )
    updated_on : Mapped[dt.datetime] = Column(
        DateTime(timezone = True), default = None,
        onupdate = dt.datetime.now()
    )

    session : Mapped[list["SessionRecord"]] = relationship(
        "SessionRecord", back_populates = "project",
        cascade = "all, delete-orphan", passive_deletes = True
    )


class SessionRecord(BaseSchema):
    """
    ORM Mapping for the ``apt_session`` Table in a Relational DB
    """

    __tablename__ = "apt_session"
    __table_args__ = (
        Index("idx_apt_sessions_project_id", "project_id")
    )

    session_id : Mapped[str] = Column(String(36), primary_key = True)
    project_id : Mapped[str] = Column(
        String(36),
        ForeignKey("apt_project.job_name", ondelete = "CASCADE"),
        nullable = False
    )

    scheduled_by : Mapped[str] = Column(
        String(36), nullable = False
    )

    created_on : Mapped[dt.datetime] = Column(
        DateTime(timezone = True), nullable = False,
        default = dt.datetime.now()
    )
    updated_on : Mapped[dt.datetime] = Column(
        DateTime(timezone = True), default = None,
        onupdate = dt.datetime.now()
    )

    project : Mapped["ProjectRecord"] = relationship(
        "ProjectRecord", back_populates = "sessions"
    )
