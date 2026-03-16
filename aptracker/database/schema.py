# -*- encoding: utf-8 -*-

"""
SQL Alchemy ORM Schema Definitions for APTracker

Declares relational database tables that backs the :mod:`APTracker`
persistence layer using :mod:`SQLAlchemy` ORM framework. All objects
(tables, functions, etc.) are prefixed with ``apt_`` to avoid name
collision when the module shares the database with other application.
"""

import datetime as dt

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    String, DateTime, Index, ForeignKey, Boolean, Integer
)

from aptracker._base.schema import BaseSchema

class ProjectRecord(BaseSchema):
    """
    ORM Mapping for the ``apt_project`` Table in a Relational DB
    """

    __tablename__ = "apt_project"

    job_id : Mapped[str] = mapped_column(
        String(36), primary_key = True
    )
    job_name : Mapped[str] = mapped_column(
        String(128), unique = True, nullable = False
    )

    created_on : Mapped[dt.datetime] = mapped_column(
        DateTime(timezone = True), nullable = False,
        default = dt.datetime.now()
    )
    updated_on : Mapped[dt.datetime] = mapped_column(
        DateTime(timezone = True), nullable = True, default = None,
        onupdate = dt.datetime.now()
    )

    is_active : Mapped[bool] = mapped_column(
        Boolean, nullable = False, default = True
    )


class SessionRecord(BaseSchema):
    """
    ORM Mapping for the ``apt_session`` Table in a Relational DB
    """

    __tablename__ = "apt_session"
    __table_args__ = (
        Index("idx_apt_sessions_job_id", "job_id"),
        Index("idx_apt_sessions_session_id", "session_id"),
    )

    session_id : Mapped[str] = mapped_column(
        String(36), primary_key = True
    )
    session_name : Mapped[str] = mapped_column(
        String(128), nullable = False
    )

    job_id : Mapped[str] = mapped_column(
        String(36),
        ForeignKey("apt_project.job_id", ondelete = "CASCADE"),
        nullable = False
    )

    created_on : Mapped[dt.datetime] = mapped_column(
        DateTime(timezone = True), nullable = False,
        default = dt.datetime.now()
    )

    created_by : Mapped[str] = mapped_column(
        String(36), nullable = False
    )

    scheduled_on : Mapped[dt.datetime] = mapped_column(
        DateTime(timezone = True), nullable = False,
        default = dt.datetime.now()
    )

    next_scheduled_on : Mapped[dt.datetime] = mapped_column(
        DateTime(timezone = True), nullable = True
    )

    decommissioned_on : Mapped[dt.datetime] = mapped_column(
        DateTime(timezone = True), nullable = True, default = None,
        onupdate = dt.datetime.now()
    )

    decommissioned_by : Mapped[str] = mapped_column(
        String(36), nullable = True
    )


class EventLogs(BaseSchema):
    """
    ORM Mapping for the ``apt_events`` Table in a Relational DB
    """

    __tablename__ = "apt_events"
    __table_args__ = (
        Index("idx_apt_events_session_id", "session_id"),
    )

    event_id : Mapped[int] = mapped_column(
        Integer, primary_key = True, autoincrement = True
    )

    session_id : Mapped[str] = mapped_column(
        String(36),
        ForeignKey("apt_session.session_id", ondelete = "CASCADE"),
        nullable = False
    )

    message : Mapped[str] = mapped_column(
        String(1024), nullable = False
    )

    # all the below are for exception handling, defaults to None
    exception_type : Mapped[str] = mapped_column(
        String(64), nullable = True
    )
    exception_value : Mapped[str] = mapped_column(
        String(128), nullable = True
    )
    exception_traceback : Mapped[str] = mapped_column(
        String(1024), nullable = True
    )

    created_on : Mapped[dt.datetime] = mapped_column(
        DateTime(timezone = True), nullable = False,
        default = dt.datetime.now()
    )
