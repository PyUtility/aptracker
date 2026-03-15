# -*- encoding: utf-8 -*-

"""
Track a project that has multiple instances or sessions running in a
production environment using session managers that can be used to set
an unique identity and can be tracked from a centralized system.
"""

import os
import getpass
import subprocess
import datetime as dt

from uuid import uuid4 as UUIDx
from dataclasses import dataclass

@dataclass(frozen = True)
class SessionConfig:
    """
    A Strictly Frozen Data Class for to Handle Sessions of a Project

    A session of a job/project can be running instances or schedules
    on a production environment. The session can be tracked using a
    unique key and can be referenced back to the project.

    :type  JOB_ID: str
    :param JOB_ID: A unique job identity key, defaults to ``UUID``
        that can be used for a particular project. This will be used
        as a primary key in the database. The alternate is the name
        of the job/project which is uniquely defined during the
        project creation.

    :type  SESSION_ID: str
    :param SESSION_ID: A unique session identity key, defaults to
        ``UUID`` that can be used for a particular project.

    :type  CREATED_ON: dt.datetime
    :param CREATED_ON: The date and time when the session was
        created, defaults to ``dt.datetime.now()`` value. The value
        can be different from the scheduled date and time of the job
        execution based on the session manager.

    :type  CREATED_BY: str
    :param CREATED_BY: Name of the user, machine or instance where
        the session was created. Defaults to ``getpass.getuser()``
        for the current environment.

    :type  ENVIRONMENT: str
    :param ENVIRONMENT: Environment details, defaults to ``dev``. Any
        values can be set and there is no restriction.

    :type  VERBOSEMODE: bool
    :param VERBOSEMODE: Verbose details into console when True
        (default) during post initialization.

    The data class is defined as ``frozen`` as once initialized this
    value should not be changed or altered. Example usage:

    .. code-block:: python

        import aptracker as apt

        session = apt.SessionConfig(JOB_ID = "ABC...")
        >> Session ID : ABC... Crated for 'ABC...' at ...
    """

    JOB_ID : str = str(UUIDx()).upper()

    # ? global frozen values for a project run, with default values
    SESSION_ID : str = str(UUIDx()).upper()

    # ? controller for the session, created on, created by can be
    # different from the scheduled date and time of execution
    CREATED_ON : dt.datetime = dt.datetime.now()
    CREATED_BY : str = getpass.getuser()

    # ? control for environment, verbose statements
    ENVIRONMENT : str = "dev"
    VERBOSEMODE : bool = True


    @property
    def PROJECT_ROOT(self) -> str:
        """
        Define Root Directory for the Project if Version Controlled

        The root of the project can be defined directly, if version
        controlled using ``git``, else sets to the current directory.
        The value is always absolute path to the project.
        """

        root = os.path.join(subprocess.Popen(
            ['git', 'rev-parse', '--show-toplevel'],
            stdout=subprocess.PIPE
        ).communicate()[0].rstrip().decode('utf-8'))

        return root or os.path.abspath(os.path.dirname(__file__))


    def __post_init__(self) -> None:
        """
        Post Session Initialization Verbose Details into Console/Log

        When a session is created, log details into console about the
        session and other important attributes. Useful in development
        environment, can be toggled based on object.
        """

        statement = f"Session ID : {self.SESSION_ID} " \
            + f"Created for '{self.JOB_ID}' at {self.CREATED_ON}"
        
        if self.VERBOSEMODE:
            print(statement)
        else:
            pass

        return


    def __repr__(self) -> str:
        return f"JOB_ID: {self.JOB_ID} SESSION_ID: {self.SESSION_ID}"
