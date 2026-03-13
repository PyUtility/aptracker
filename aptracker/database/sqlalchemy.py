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
        verbose : bool = False
    ) -> None:
        engine = create_async_engine(engine, echo = verbose)

        logger_ = logger or logging.getLogger(__name__)
        super().__init__(engine = engine, logger = logger_)

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

        async with self.engine.begin() as conn:
            await conn.run_sync(BaseSchema.metadata.create_all)

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


    async def create(
        self,
        session : SessionConfig,
        description : str
    ) -> str:
        """
        Register a new project in the database using the session
        configuration parameter and add the data to the underlying.

        :type  session: SessionConfig
        :param session: Session configuration, a frozen data class
            that is initialized to handle the sessions of a project.

        :type  description: str
        :param description: An unique human redable project name for
            the project. The session configuration does not use the
            project name field, instead refers to the job name which
            is typically a unique identifier for the project.
        """

        now = dt.datetime.now(tz = dt.timezone.utc)
        job_name = session.JOB_NAME # frozen name; type: ignore

        async with self._session_factory() as db_session:
            db_session.add(ProjectRecord(
                job_name = job_name,
                job_description = description,
                created_on = now
            ))

            await db_session.commit()

        return job_name


    async def register(
        self,
        session : SessionConfig,
        description : str
    ) -> str:
        """
        Register a new project session, this session is unique that
        can be used to uniquely identify the project details - like
        report builder, development checks, chore runs, etc.

        :type  session: SessionConfig
        :param session: Session configuration, a frozen data class
            that is initialized to handle the sessions of a project.

        :type  description: str
        :param description: A human redable session description that
            can be used to identify the session. The value is not
            unique as same type of jobs can have the same name. The
            value is not used by the session config, and must be
            passed individually to the register method.
        """

        job_name = session.JOB_NAME # frozen name; type: ignore

        async with self._session_factory() as db_session:
            db_session.add(SessionRecord(
                session_id = session.SESSION_ID,
                project_id = job_name,
                session_name = description,
                scheduled_by = session.SCHEDULED_BY,
                created_on = session.SCHEDULED_ON
            ))

            await db_session.commit()

        return job_name


    async def eventlogger(self, session : SessionConfig) -> str:
        pass
