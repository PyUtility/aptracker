# -*- encoding: utf-8 -*-

"""
Abstract Asynchronous Database Interface for APTracker

The abstract contract that all database backends must implement the
from the abstract database interface. The interface is intentionally
backend-agnostic so that concrete subclasses can target any
persistence layer - relational (e.g., PostgreSQL, SQLite, etc.) or
any non-relational (e.g., DynamoBD, MongoDB, etc.) without altering
the calling code.

All I/O methods are declared as ``async`` coroutines. Implementations
must never perform blocking I/O inside them. The defined context
managers supports (``async with``) which is provided at the base.
"""

import abc
import logging

from aptracker.session import SessionConfig

class BaseDatabase(abc.ABC):
    """
    Abstract Asynchronous Database Interface for APTracker

    Provides the contract that every database backend must fulfill to
    integrate with the APTracker project-tracking system. The class
    defines connection-lifecycle hooks, async context-manager support,
    and abstract CRUD coroutines for projects, sessions, and events.

    :type  engine: object
    :param engine: Database engine or asynchronous connection pool.
        The concrete type depends on the chosen backend.

    :type  logger: logging.Logger
    :param logger: Standard logger for recording operational events.
        Callers should supply a named logger to enable structured log
        filtering using wrappers.
    """

    def __init__(
        self,
        engine : object,
        logger : logging.Logger
    ) -> None:
        """
        Initialization Method for Database Backends

        The class should be able to seamlessly integrated with any
        backend data frameworks and must implement the asynchronous
        calling contracts defined in the abstract class. The class
        has the following methods:

            * :meth:`connect`: Initialize underlying connection pool
                or establish a persistent connection to the database.

            * :meth:`disconnect`: Close underlying connection pool or
                persistent connection to the database.

            * :meth:`__aenter__`: Asynchronous context manager entry
                point that delegates :meth:`connect` to a block.

            * :meth:`__aexit__`: Asynchronous context manager exit
                point that delegates :meth:`disconnect` by releasing
                all resouces held by the connection block.
        """

        self.engine = engine
        self.logger = logger

        # connection status, should be False, implement in connect()
        self._status = False


    @abc.abstractmethod
    async def connect(self, *args, **kwargs) -> None:
        """
        Initialize underlying connection pool or establish a
        persistent connection to the database. Implementations must be
        idempotent - repeated calls while already connected.
        """

        pass


    @abc.abstractmethod
    async def disconnect(self, *args, **kwargs) -> None:
        """
        Close underlying connection pool or persistent connection to
        the database. The method should be able to release all the
        resources held by the connection pool or a single connection.

        Asfter a disconnect method is called, any query must raise an
        ``RuntimeError`` or implementation must try to reconnect
        automatically on the next awaited call.
        """

        pass


    async def __aenter__(self) -> "BaseDatabase":
        """
        Asynchronous context manager entry point that delegates
        :meth:`connect` and returns ``self`` so the instance can be
        used directly inside an ``async with`` block.
        """

        await self.connect()
        return self


    async def __aexit__(
        self,
        exec_type : type | None,
        exec_value : BaseException | None,
        exec_traceback : type | None
    ) -> None:
        """
        Asynchronous context manager exit point that delegates
        :meth:`disconnect` unconditionally, ensuring that the
        connections are never leaked regardless of whether the block
        raised an exception.

        Typically the method should be able to handle all types of
        exceptions raised by the block, and close the pool. Typical
        block should have the following form:

        :type  exec_type: type | None
        :param exec_type: An exception class on error; should be
            ``None`` on a clean exit.

        :type  exec_value: BaseException | None
        :param exec_value: An exception value on error; should be
            ``None`` on a clean exit.

        :type  exec_traceback: type | None
        :param exec_traceback: An exception traceback on error;
            should be ``None`` on a clean exit.

        The method follows a fixed signature, and type checkers can
        verify that the signature matches the protocol.
        """

        await self.disconnect()
        return


    @property
    async def status(self) -> bool:
        """
        Connection status readiness flag, returns ``True`` when the
        connection is open and ready to accept queries; else returns
        ``False``, use to check if a query should be attempted.
        """

        return self._status


    @abc.abstractmethod
    async def create(self, session : SessionConfig) -> str:
        """
        Register a new project, this should use the session
        configuration and any atribute associated with the session
        can be used directly in the query.

        :type  session: SessionConfig
        :param session: A frozen data class that is initialized to
            handle the sessions of a project.
        """

        pass


    @abc.abstractmethod
    async def register(self, session : SessionConfig) -> str:
        """
        Register a new session for the underlying defined/created
        project, this should use the session configuration and any
        atribute associated with the session can be used directly.

        :type  session: SessionConfig
        :param session: A frozen data class that is initialized to
            handle the sessions of a project.
        """

        pass


    @abc.abstractmethod
    async def eventlogger(self, session : SessionConfig) -> str:
        """
        Append a event tracker to a session. Each call records a
        discrete activity within the session, enabling fine-grained
        progress tracking and post-analysis.
        """

        pass
