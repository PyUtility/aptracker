# -*- encoding: utf-8 -*-

"""
SQLAlchemy Asynchronous Implementation of BaseDatabase for APTracker
"""

import logging
import datetime as dt

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from aptracker.session import SessionConfig
from aptracker._base.schema import BaseSchema
from aptracker._base.database import BaseDatabase

from aptracker.database.schema import (
    ProjectRecord,
    SessionRecord
)

class SQLAlchemyDB(BaseDatabase):
    """
    SQLAlchemy Asynchronous Backend for APTracker

    Wraps an :class:`~sqlalchemy.ext.asyncio.AsyncEngine` and exposes
    the full :class:`~aptracker._base.database.BaseDatabase` contract
    as awaitable coroutines. A single instance is safe to share
    across concurrent tasks because SQLAlchemy's async session factory
    creates a new :class:`~sqlalchemy.ext.asyncio.AsyncSession`
    per operation. Example usage:

    .. code-block:: python

        async with SQLAlchemyDB(engine = ...) as db:
            project_id =await db.create(session)
    """

    def __init__(
        self,
        engine : str,
        logger : logging.Logger,
        session : SessionConfig,
        verbose : bool = False
    ) -> None:
        engine = create_async_engine(engine, echo = verbose)

        logger_ = logger or logging.getLogger(__name__)
        super().__init__(
            engine = engine, logger = logger_, session = session
        )

        # session factory object
        self._session_factory : async_sessionmaker[AsyncSession] = \
            async_sessionmaker(
                bind = self.engine,
                expire_on_commit = False
            )


    async def connect(self) -> None:
        """
        Open the connection and bootstrap the schema, create tables
        on first use for all APTracker tables against the configured
        database engine.
        """

        async with self.engine.begin() as conn: # type: ignore
            await conn.run_sync(
                BaseSchema.metadata.create_all
            )

        self._status = True
        self.logger.info(
            f"APTracker Database Connected to {self.engine.url}"
        )

        return


    async def disconnect(self) -> None:
        """
        Safely dispose the connection poll and marks the instance as
        disconnected. To reconnect, call :meth:`connect` again.
        """

        await self.engine.dispose()
        self._status = False

        self.logger.info("APTracker Database Disconnected")
        return


    async def create(self, job_name : str) -> str:
        """
        Register a new project in the database using the session
        configuration parameter and add the data to the underlying.

        :type  job_name: str
        :param job_name: An unique human redable project name for
            the project. The session configuration does not use the
            job name field, instead refers to the job id which is
            typically a unique identifier for the project.
        """

        now = dt.datetime.now(tz = dt.timezone.utc)
        retvalue = f"ID: {self.job_id} Job Name: {job_name}"

        async with self._session_factory() as db_session:
            db_session.add(ProjectRecord(
                job_id = self.job_id,
                job_name = job_name,
                created_on = now
            ))

            await db_session.commit()

        return retvalue


    async def register(self, session_name : str, **kwargs) -> str: # type: ignore
        """
        Register a new project session, this session is unique that
        can be used to uniquely identify the project details - like
        report builder, development checks, chore runs, etc.

        :type  session_name: str
        :param session_name: A human redable session description that
            can be used to identify the session. The value is not
            unique as same type of jobs can have the same name. The
            value is not used by the session config, and must be
            passed individually to the register method.

        The following optional keywords arguments are accepted, if
        not passed defaults to database defaults (if any):

            * ``scheduled_on`` (:class:`~datetime.datetime`): The
              date and time when the session was scheduled to be
              executed, if not passed defaults to database defaults.

            * ``next_scheduled_on`` (:class:`~datetime.datetime`): The
              date and time when the session is scheduled to be
              executed next, this is nullable and defaults to None.
        """

        now = dt.datetime.now(tz = dt.timezone.utc)
        retvalue = f"ID: {self.job_id} Session ID: {self.session_id}"

        async with self._session_factory() as db_session:
            db_session.add(SessionRecord(
                session_id = self.session_id,
                session_name = session_name,
                job_id = self.job_id,
                created_on = self.session.CREATED_ON,
                created_by = self.session.CREATED_BY,
                scheduled_on = kwargs.get("scheduled_on", now),
                next_scheduled_on = kwargs.get("next_scheduled_on", None)
            ))

            await db_session.commit()

        return retvalue


    async def eventlogger(self) -> str: # type: ignore
        pass
