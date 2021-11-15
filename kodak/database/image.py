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
        extension = path.suffix

        for item in constants.ImageFormat:
            if extension.replace(".", "") in item.value:
                format_ = item
                break
        else:
            raise RuntimeError

        name = str(path.relative_to(config.source_dir)).replace(
            os.sep, constants.IMAGE_PATH_NAME_SEPARATOR
        )[: -len(extension)]

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
        Path(config.content_dir, self.name).mkdir(exist_ok=True)
        link = Path(config.content_dir, self.name, "original")
        try:
            link.symlink_to(config.source_dir / self.source)
        except FileExistsError:
            pass
        return link

    def remove_link(self, config: configuration.KodakConfig) -> None:
        """Remove a link between the content and source directory

        :param config: Populated application configuration object
        """
        Path(config.content_dir, self.name, "original").unlink(missing_ok=True)
