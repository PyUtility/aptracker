# -*- encoding: utf-8 -*-

"""
Example of Main File Configuration for using APTracker Module

This is a simple example of main file that creates a new session, and
uses SQLite as the database backend. The backend tables are populated
with a new project and a new session is recorded for the project.
"""

import uuid
import asyncio
import logging

from aptracker.session import SessionConfig
from aptracker.database.sqlalchemy import SQLAlchemyDB

async def main(session : SessionConfig) -> None:
    job_name = f"[{str(uuid.uuid4()).upper()[:3]}] Example Project"
    session_name = f"[{str(uuid.uuid4()).upper()[:3]}] Example Session"

    logging.basicConfig(level = logging.INFO)
    logger = logging.getLogger("aptracker")

    async with SQLAlchemyDB(
        engine = "sqlite+aiosqlite:///example.db",
        logger = logger, session = session, verbose = True
    ) as db:
        statement = await db.create(job_name = job_name)

        print(f"Created Project: {statement}")

        statement = await db.register(
            session_name = session_name
        )

        print(f"Created Session: {statement}")

        statement = await db.eventlogger(
            message = "Test Message"
        )


if __name__ == "__main__":
    session = SessionConfig()
    asyncio.run(main(session = session))
