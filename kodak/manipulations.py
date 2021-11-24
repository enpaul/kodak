import logging

from PIL import Image

from kodak import configuration
from kodak import constants


def scale(image: Image.Image, config: configuration.ManipConfig) -> Image.Image:
    """Scale an image to new dimensions"""

    if config.scale.strategy == constants.ScaleStrategy.ABSOLUTE:
        width = config.scale.horizontal or image.width
        height = config.scale.vertical or image.height
    elif config.scale.strategy == constants.ScaleStrategy.RELATIVE:
        width = (
            (config.scale.horizontal * image.width)
            if config.scale.vertical
            else image.width
        )
        height = (
            (config.scale.horizontal * image.height)
            if config.scale.vertical
            else image.height
        )
    else:
        raise ValueError("Here there be dragons")

    logging.getLogger(__name__).debug(
        f"Scaling image: old {image.width}x{image.height}; new {width}x{height})"
    )

    if config.scale.horizontal is None or config.scale.vertical is None:
        image = image.copy()
        image.thumbnail((width, height), Image.ANTIALIAS)
    else:
        image.resize((width, height))

    return image


def crop(image: Image.Image, config: configuration.ManipConfig) -> Image.Image:
    """Crop an image to new dimensions"""

    # TODO: add safeguards for when config values are out of bounds for the image

    width = config.crop.horizontal or image.width
    height = config.crop.vertical or image.height

    if config.crop.anchor == constants.CropAnchor.TL:
        x_1 = 0
        y_1 = 0
        x_2 = width
        y_2 = height
    elif config.crop.anchor == constants.CropAnchor.TC:
        x_1 = (image.width / 2) - (width / 2)
        y_1 = 0
        x_2 = (image.width / 2) + (width / 2)
        y_2 = height
    elif config.crop.anchor == constants.CropAnchor.TR:
        x_1 = image.width - width
        y_1 = 0
        x_2 = image.width
        y_2 = height
    elif config.crop.anchor == constants.CropAnchor.CL:
        x_1 = 0
        y_1 = (image.height / 2) - (height / 2)
        x_2 = width
        y_2 = (image.height / 2) + (height / 2)
    elif config.crop.anchor == constants.CropAnchor.C:
        x_1 = (image.width / 2) - (width / 2)
        y_1 = (image.height / 2) - (height / 2)
        x_2 = (image.width / 2) + (width / 2)
        y_2 = (image.height / 2) + (height / 2)
    elif config.crop.anchor == constants.CropAnchor.BL:
        x_1 = 0
        y_1 = image.height - height
        x_2 = width
        y_2 = image.height
    elif config.crop.anchor == constants.CropAnchor.BC:
        x_1 = (image.width / 2) - (width / 2)
        y_1 = image.height - height
        x_2 = (image.width / 2) + (width / 2)
        y_2 = image.height
    elif config.crop.anchor == constants.CropAnchor.BR:
        x_1 = image.width - width
        y_1 = image.height - height
        x_2 = image.width
        y_2 = image.height
    else:
        raise ValueError("Ye gadds! This codepath is impossible!")

    logging.getLogger(__name__).debug(
        f"Cropping image: old {image.width}x{image.height}; new {width}x{height}; upper-0 anchor ({x_1}, {y_1}); lower-image.width anchor ({x_2}, {y_2})"
    )

    return image.crop((x_1, y_1, x_2, y_2))


def black_and_white(
    image: Image.Image,
    config: configuration.ManipConfig,  # pylint: disable=unused-argument
) -> Image.Image:
    """Convert an image to full-depth black and white"""
    logger = logging.getLogger(__name__)
    logger.debug("Converting image to black and white")
    return image.convert("L")
