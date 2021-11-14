import logging
from typing import Sequence
from typing import Tuple
from typing import Type

import peewee

from kodak import constants
from kodak import exceptions
from kodak.configuration import KodakConfig
from kodak.database._shared import Checksum
from kodak.database._shared import INTERFACE as interface
from kodak.database._shared import KodakModel
from kodak.database.access import AccessRecord
from kodak.database.image import ImageRecord
from kodak.database.manip import ManipRecord


MODELS: Tuple[Type[KodakModel], ...] = (ImageRecord, ManipRecord, AccessRecord)


def calc_batch_size(
    backend: constants.DatabaseBackend, models: Sequence[KodakModel]
) -> int:
    """Determine the batch size that should be used when performing queries

    This is intended to work around the query variable limit in SQLite. Critically this is a
    limit to the number of _variables_, not _records_ that can be referenced in a single query.

    The "correct" way to calculate this is to iterate over the model list and tally the number of
    changed fields, then add one for the table name, and each time you reach the
    ``SQLITE_VARIABLE_LIMIT`` (which is a known constant) cut a new batch until all the models are
    processed. This is very complicated because peewee doesn't provide a simple way to reliably
    identify changed fields.

    The naive way to calculate this (i.e. the way this function does it) is to determine the
    maximum number of variables that _could be_ used to modify a record and use that as the
    constant batch limiter. The theoretical maximum number of variables associated with a single
    record is equal to the number of fields on that record, plus 1 (for the table name). This gives
    the batch size (i.e. number of records that can be modified in a single query) as:

    ::

      999 / (len(fields) + 1)

    Where ``fields`` is an array of the fields that could be written on the record.

    .. note:: This function (pretty safely) assumes that all the records in ``models`` are of the
              same model type; i.e. they all relate to the same table. This is a pretty safe
              assumption since there's no way to do multi-table updates in a single query while
              using sane SQL practices.

    .. note:: This function just returns ``len(models)`` if the backend is anything other than
              ``SQLITE``. This is because the limitation this works around is only applicable to
              SQLite so on other platforms we can just make the batch size as large as possible.

    :param backend: Backend being used by the application
    :param models: Sequence of models that need to be batched
    :returns: Number of models that can be processed in a single batch
    """
    # oof, the ratio of lines-of-docstring to lines-of-code in this function is 35:3
    if models and backend == constants.DatabaseBackend.SQLITE:
        return int(constants.SQLITE_VARIABLE_LIMIT / (len(models[0].fields) + 1))
    return len(models)


def initialize(config: KodakConfig):
    """Initialize the database interface

    Defining the database as an
    `unconfigured proxy object <http://docs.peewee-orm.com/en/latest/peewee/database.html#setting-the-database-at-run-time>`_
    allows it to be configured at runtime based on the config values.

    :param config: Populated configuration container object
    """

    logger = logging.getLogger(__name__)

    if config.database.backend == constants.DatabaseBackend.SQLITE:
        logger.debug("Using SQLite database backend")
        logger.debug(f"Applying SQLite pragmas: {config.database.sqlite.pragmas}")
        database = peewee.SqliteDatabase(
            config.database.sqlite.path, pragmas=config.database.sqlite.pragmas
        )
    elif config.database.backend == constants.DatabaseBackend.MARIADB:
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
        raise exceptions.ConfigurationError(
            f"Invalid storage backend in configuration: {config.database.backend}"
        )

    interface.initialize(database)

    with interface.atomic():
        interface.create_tables(MODELS)
