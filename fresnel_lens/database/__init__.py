import logging
from typing import Tuple

import peewee

from fresnel_lens import constants
from fresnel_lens.configuration import FresnelConfig
from fresnel_lens.database._shared import FresnelModel
from fresnel_lens.database._shared import INTERFACE as interface
from fresnel_lens.database.image import ImageRecord
from fresnel_lens.database.thumbnail import ThumbnailRecord


MODELS: Tuple[FresnelModel, ...] = (ImageRecord, ThumbnailRecord)


def initialize(config: FresnelConfig):
    """Initialize the database interface

    Defining the database as an
    `unconfigured proxy object <http://docs.peewee-orm.com/en/latest/peewee/database.html#setting-the-database-at-run-time>`_
    allows it to be configured at runtime based on the config values.

    :param config: Populated configuration container object
    """

    logger = logging.getLogger(__name__)

    if config.database.backend == constants.SupportedDatabaseBackend.SQLITE:
        logger.debug("Using SQLite database backend")
        logger.debug(f"Applying SQLite pragmas: {config.database.sqlite.pragmas}")
        database = peewee.SqliteDatabase(
            config.database.sqlite.path, pragmas=config.database.sqlite.pragmas
        )
    elif config.database.backend == constants.SupportedDatabaseBackend.MARIADB:
        logger.debug("Using MariaDB database backend")
        logger.debug(
            "Configuring MariaDB:"
            f" {config.database.mariadb.username}@{config.database.mariadb.hostname}:{config.database.mariadb.port},"
            f" with database '{config.database.mariadb.schema}'"
        )
        database = peewee.MySQLDatabase(
            config.database.mariadb.schema,
            host=config.database.mariadb.hostname,
            port=config.database.mariadb.port,
            user=config.database.mariadb.username,
            password=config.database.mariadb.password,
            charset="utf8mb4",
        )
    else:
        raise ValueError(
            f"Invalid storage backend in configuration: {config.database.backend}"
        )

    interface.initialize(database)

    with interface.atomic():
        interface.create_tables(MODELS)
