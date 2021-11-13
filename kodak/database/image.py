import hashlib
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

        .. note:: This method attempts to _efficiently_ compute a hash of large image files. The
                  hashing code was adapted from here:

                  https://stackoverflow.com/a/44873382/5361209
        """
        hasher = hashlib.sha256()
        view = memoryview(bytearray(1024 * 1024))
        with path.open("rb", buffering=0) as infile:
            for chunk in iter(lambda: infile.readinto(view), 0):  # type: ignore
                hasher.update(view[:chunk])

        name = path.stem
        extension = path.suffix

        for item in constants.ImageFormat:
            if extension.lower()[1:] in item.value:
                format_ = item
                break
        else:
            raise RuntimeError

        name = name.replace(str(config.source_dir), "").replace(
            os.sep, constants.IMAGE_PATH_NAME_SEPARATOR
        )

        return cls(
            name=name, source=path, format_=format_, checksum=Checksum.from_hash(hasher)
        )

    def create_link(self, config: configuration.KodakConfig) -> Path:
        """Creates a link between the content directory and source directory

        :param config: Populated application configuration object
        :returns: Path to the created symbolic link back to the source file
        """
        link = Path(config.content_dir, self.name)
        try:
            link.symlink_to(self.source)
        except FileExistsError:
            pass
        return link

    def remove_link(self, config: configuration.KodakConfig) -> None:
        """Remove a link between the content and source directory

        :param config: Populated application configuration object
        """
        Path(config.content_dir, self.name).unlink(missing_ok=True)
