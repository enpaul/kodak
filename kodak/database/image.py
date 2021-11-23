import logging
import os
from pathlib import Path

import peewee

from kodak import configuration
from kodak import constants
from kodak.database._shared import Checksum
from kodak.database._shared import ChecksumField
from kodak.database._shared import EnumField
from kodak.database._shared import KodakModel
from kodak.database._shared import PathField


class ImageRecord(KodakModel):
    """Model for source images"""

    name = peewee.CharField(null=False)
    source = PathField(null=False)
    format_ = EnumField(constants.ImageFormat, null=False)
    deleted = peewee.BooleanField(null=False, default=False)
    checksum = ChecksumField(null=False)

    @classmethod
    def from_path(cls, config: configuration.KodakConfig, path: Path):
        """Construct an image record from a path

        :param config: Populated application configuration object
        :param path: Full path to the image file to process. The file path provided is expected to
                     already be absolute, with all symlinks and aliases resolved.
        """
        logger = logging.getLogger(__name__)

        logger.debug(f"Creating image record from path {path}")

        extension = path.suffix
        for item in constants.ImageFormat:
            if extension.replace(".", "").lower() in item.value:
                format_ = item
                logger.debug(
                    f"Identified format of file {path} as '{format_.name}' based on file extension"
                )
                break
        else:
            raise RuntimeError

        name = str(path.relative_to(config.source_dir)).replace(
            os.sep, constants.IMAGE_PATH_NAME_SEPARATOR
        )[: -len(extension)]

        logger.debug(f"Determined image name of file {path} to be '{name}'")

        return cls(
            name=name,
            source=path.relative_to(config.source_dir),
            format_=format_,
            checksum=Checksum.from_path(path),
        )

    def create_link(self, config: configuration.KodakConfig) -> Path:
        """Creates a link between the content directory and source directory

        :param config: Populated application configuration object
        :returns: Path to the created symbolic link back to the source file
        """
        logger = logging.getLogger(__name__)

        Path(config.content_dir, self.name).mkdir(exist_ok=True)
        link = Path(config.content_dir, self.name, "original")
        try:
            link.symlink_to(config.source_dir / self.source)
            logger.debug(
                f"Created link from {config.source_dir / self.source} to {link}"
            )
        except FileExistsError:
            pass
        return link

    def remove_link(self, config: configuration.KodakConfig) -> None:
        """Remove a link between the content and source directory

        :param config: Populated application configuration object
        """
        logger = logging.getLogger(__name__)
        link = Path(config.content_dir, self.name, "original")
        link.unlink(missing_ok=True)
        logger.debug(f"Removed link from {config.source_dir / self.source} to {link}")
