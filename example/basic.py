# -*- encoding: utf-8 -*-

"""
Example of Main File Configuration for using APTracker Module

This is a simple example of main file that creates a new session, and
uses SQLite as the database backend. The backend tables are populated
with a new project and a new session is recorded for the project.
"""

import os
import sys

import uuid
import asyncio
import logging

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
))

from aptracker.session import SessionConfig
from aptracker.database.sqlalchemy import SQLAlchemyDB

async def main(session : SessionConfig) -> None:
    session_name = "Example Session"
    project_name = f"[{str(uuid.uuid4())[:3]}] Example Project"

    logging.basicConfig(level = logging.INFO)
    logger = logging.getLogger("aptracker")

    async with SQLAlchemyDB(
        engine = "sqlite+aiosqlite:///example.db",
        logger = logger, verbose = True
    ) as db:
        project_id = await db.create(
            session = session, description = project_name
        )

        _ = await db.register(
            session = session, description = session_name
        )

        print(f"Project ID: {project_id}")


if __name__ == "__main__":
    session = SessionConfig(
        JOB_NAME = str(uuid.uuid4()).upper()
    )

    asyncio.run(main(session = session))
