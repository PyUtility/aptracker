# -*- encoding: utf-8 -*-

"""
A Set of Context Managers for APTracker Module

The context managers provide objects to handle operations easily. The
:class:`APTTerminalClient` is designed to work in any terminal
environment providing ease of operation by just calling one single
function once initialized.
"""

import logging

from typing import Any, Dict, Optional

from aptracker.database.sqlalchemy import SQLAlchemyDB

class APTTerminalClient:
    def __init__(self, engine : str, session : str) -> None:
        self.engine = engine
        self.session = session

        # ? create a default logger; todo send logger during init
        logging.basicConfig(level = logging.INFO)
        self.logger = logging.getLogger("APTracker")


    async def perform(self, operation : str, **kwargs) -> Optional[Any]: # type: ignore
        """
        Perform any of the Valid Operation on a given DB Engine
        """

        params : Dict[str, Dict[str, Any]] = dict(
            create = {"job_name" : kwargs.get("job_name", None)},
            register = {"session_name" : kwargs.get("session_name", None)},
            eventlogger = {"message" : kwargs.get("message", None)}
        )

        async with SQLAlchemyDB(
            engine = self.engine, logger = self.logger,
            session = self.session, verbose = False
        ) as db:
            func : Optional[Any] = dict( # type: ignore
                create = db.create,
                register = db.register, # type: ignore
                eventlogger = db.eventlogger
            )[operation]

            retvalue : Optional[Any] = await func(**params[operation])

        return retvalue
