import logging
import shutil
from pathlib import Path
from typing import List
from typing import Optional

from kodak import configuration
from kodak import constants
from kodak import database


def identify(config: configuration.KodakConfig) -> List[database.ImageRecord]:
    """Identify source images that will be made available

    :param config: Populated application configuration object
    :returns: List of (unsaved) database models representing identified source image files
    """

    def _identify(path: Path) -> List[Path]:
        identified = []
        for item in path.iterdir():
            if item.is_file() and item.suffix in constants.IMAGE_FILE_EXTENSIONS:
                logger.debug(f"Including file {item}")
                identified.append(item.resolve())
            elif item.is_dir():
                logger.debug(f"Entering subdirectory {item}")
                identified += _identify(item)
            else:
                logger.debug(f"Skipping {item}")
        return identified

    logger = logging.getLogger(__name__)

    logger.info(
        f"Identifying image files with extensions {', '.join(constants.IMAGE_FILE_EXTENSIONS)} under {config.source_dir}"
    )

    images = _identify(config.source_dir)

    logger.info(f"Identified {len(images)} files under {config.source_dir}")

    with database.interface.atomic():
        existing = [
            item.source
            for item in database.ImageRecord.select(database.ImageRecord.source)
        ]

    logger.debug(f"Fetched {len(existing)} existing image records")

    results = []
    for image in images:
        if image.relative_to(config.source_dir) in existing:
            logger.debug(f"Skipping existing {image}")
        else:
            logger.debug(f"Including newly identified image {image}")
            results.append(database.ImageRecord.from_path(config, image))

    return results


def clean(config: configuration.KodakConfig) -> List[database.ImageRecord]:
    """Identify removed or changed source images and mark them as deleted

    :param config: Populated application configuration object
    :returns: List of (unsaved) database models representing source images that have been deleted
              or removed
    """

    logger = logging.getLogger(__name__)

    with database.interface.atomic():
        existing = database.ImageRecord.select(database.ImageRecord.source).where(
            database.ImageRecord.deleted  # pylint: disable=singleton-comparison
            == False
        )

    logger.info(f"Identified {len(existing)} existing image records")

    deleted = []
    for item in existing:
        if (config.source_dir / item.source).exists():
            logger.debug(
                f"Image file exists, record will not be modified: {item.source}"
            )
        else:
            logger.debug(f"Image file removed, record will be deleted: {item.source}")
            item.deleted = True
            deleted.append(item)

    logger.info(f"Identified {len(deleted)} image records to be marked as deleted")

    return deleted


def build(config: Optional[configuration.KodakConfig] = None) -> None:
    """Build and update the file index

    :param config: Populated application configuration object
    """
    logger = logging.getLogger(__name__)

    config = config or configuration.load()

    new_images = identify(config)
    with database.interface.atomic():
        database.ImageRecord.bulk_create(
            new_images,
            batch_size=database.calc_batch_size(config.database.backend, new_images),
        )

    removed_images = clean(config)
    with database.interface.atomic():
        database.ImageRecord.bulk_update(
            removed_images,
            fields=[database.ImageRecord.deleted],
            batch_size=database.calc_batch_size(
                config.database.backend, removed_images
            ),
        )

    logger.info(
        f"Removing generated assets for {len(removed_images)} removed image files"
    )

    for image in removed_images:
        content = config.content_dir / image.name
        logger.debug(f"Removing content directory {content}")
        shutil.rmtree(str(content))

    logger.info("Processing source links")

    with database.interface.atomic():
        for image in database.ImageRecord.select().where(
            database.ImageRecord.deleted  # pylint: disable=singleton-comparison
            == False
        ):
            if config.expose_source:
                logger.debug(f"Creating source link to {image.source}")
                image.create_link(config)
            else:
                logger.debug(f"Removing source link to {image.source}")
                image.remove_link(config)
