# -*- coding: utf-8 -*-

"""
APTracker - Advanced Python (AP) Project Tracker & Manager
==========================================================

Working on multiple projects, or want to track different projects
running in a production environment efficiently using ``aptracker``
that provides simple context managers, classes etc. with a dynamic
dashboard of the performance logs.
"""

__version__ = "v2.0.0"

# ? added init time options registrations from aptracker.api
from aptracker.api import * # noqa: F401, F403 # pyright: ignore[reportMissingImports]
