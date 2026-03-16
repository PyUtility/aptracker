# -*- encoding: utf-8 -*-

"""
Create a New Project to Track using APTracker Module using CLI

Use a database file to create a new project to to be tracked using
the module. Approprate backends (example, ``aiosqlite`` for SQLite,
etc.) needs to be configured to use the module.
"""

import asyncio
import logging

from aptracker import SessionConfig # type: ignore
from aptracker.database.sqlalchemy import SQLAlchemyDB # type: ignore

async def create(name : str, dbpath : str) -> str:
    session = SessionConfig(SESSION_ID = None) # type: ignore

    print(
        f"Initialized Job ID: {session.JOB_ID} for Job Name: {name}",
        f"\n  >> Using Database: {dbpath}"
    )

    logging.basicConfig(level = logging.INFO)
    logger = logging.getLogger("aptracker")

    async with SQLAlchemyDB(
        engine = dbpath,
        logger = logger, session = session, verbose = False
    ) as db:
        statement = await db.create(job_name = name)
        print(f"Created Project: {statement}")

    return session.JOB_ID


if __name__ == "__main__":
    job_name = input(f"Enter Project/Job Name: ")
    database = input(f"Enter Complete Patch/URI for DB: ")
    _ = asyncio.run(create(name = job_name, dbpath = database))
