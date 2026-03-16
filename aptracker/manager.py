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
            create = {"job_name" : kwargs["job_name"]},
            register = {"session_name" : kwargs["session_name"]},
            eventlogger = {"message" : kwargs["message"]}
        )

        async with SQLAlchemyDB(
            engine = self.engine, logger = self.logger,
            session = self.session, verbose = False
        ) as db:
            retvalue : Optional[Any] = dict(
                create = await db.create(**params[operation]),
                register = await db.register(**params[operation]),
                eventlogger = await db.eventlogger(**params[operation])
            )[operation]

        return retvalue
