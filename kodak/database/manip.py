import logging

import peewee
from PIL import Image

from kodak import configuration
from kodak import constants
from kodak import manipulations
from kodak.database._shared import Checksum
from kodak.database._shared import ChecksumField
from kodak.database._shared import EnumField
from kodak.database._shared import KodakModel
from kodak.database._shared import PathField
from kodak.database.image import ImageRecord


class ManipRecord(KodakModel):
    """Model for manipulated image records"""

    parent = peewee.ForeignKeyField(ImageRecord, null=False)
    name = peewee.CharField(null=False)
    file = PathField(null=False)
    format_ = EnumField(constants.ImageFormat, null=False)
    checksum = ChecksumField(null=False)

    @classmethod
    def from_parent(
        cls,
        parent: ImageRecord,
        config: configuration.KodakConfig,
        manip: configuration.ManipConfig,
        format_: constants.ImageFormat,
    ):
        """Construct an image manip record

        :param parent: Parent image record that should be manipulated
        :param config: Populated manipulation configuration object
        :param format_: Image format that the manipulation should be saved in
        :returns: Saved image manipulation record
        """
        logger = logging.getLogger(__name__)

        logger.info(
            f"Constructing manip '{manip.name}' from source file {config.source_dir / parent.source}"
        )

        filepath = (
            config.content_dir / parent.name / f"{manip.name}.{format_.name.lower()}"
        )

        with Image.open(config.source_dir / parent.source) as image:
            if manip.scale.horizontal is not None or manip.scale.vertical is not None:
                image = manipulations.scale(image, manip)

            if manip.crop.horizontal is not None or manip.crop.vertical is not None:
                image = manipulations.crop(image, manip)

            if manip.black_and_white:
                image = manipulations.black_and_white(image, manip)

            image.save(filepath, format_.name)
        logger.debug(f"Saved manipulated image at {filepath} in {format_.name} format")

        return cls(
            parent=parent,
            name=manip.name,
            file=filepath.relative_to(config.content_dir),
            checksum=Checksum.from_path(filepath),
            format_=format_,
        )
