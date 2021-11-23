import logging

from PIL import Image

from kodak import configuration
from kodak import constants


def scale(image: Image.Image, config: configuration.ManipConfig) -> Image.Image:
    pass


def crop(image: Image.Image, config: configuration.ManipConfig) -> Image.Image:
    """Crop an image to new dimensions"""

    # TODO: add safeguards for when config values are out of bounds for the image

    width = config.crop.horizontal or image.width
    height = config.crop.vertical or image.height

    top = 0
    left = 0
    bottom = image.height
    right = image.width

    if config.crop.anchor == constants.CropAnchor.TL:
        x_1 = left
        y_1 = top
        x_2 = width
        y_2 = height
    elif config.crop.anchor == constants.CropAnchor.TC:
        x_1 = (right / 2) - (width / 2)
        y_1 = top
        x_2 = (right / 2) + (width / 2)
        y_2 = height
    elif config.crop.anchor == constants.CropAnchor.TR:
        x_1 = right - width
        y_1 = top
        x_2 = right
        y_2 = height
    elif config.crop.anchor == constants.CropAnchor.CL:
        x_1 = left
        y_1 = (bottom / 2) - (height / 2)
        x_2 = width
        y_2 = (bottom / 2) + (height / 2)
    elif config.crop.anchor == constants.CropAnchor.C:
        x_1 = (right / 2) - (width / 2)
        y_1 = (bottom / 2) - (height / 2)
        x_2 = (right / 2) + (width / 2)
        y_2 = (bottom / 2) + (height / 2)
    elif config.crop.anchor == constants.CropAnchor.BL:
        x_1 = left
        y_1 = bottom - height
        x_2 = width
        y_2 = bottom
    elif config.crop.anchor == constants.CropAnchor.BC:
        x_1 = (right / 2) - (width / 2)
        y_1 = bottom - height
        x_2 = (right / 2) + (width / 2)
        y_2 = bottom
    elif config.crop.anchor == constants.CropAnchor.BR:
        x_1 = right - width
        y_1 = bottom - height
        x_2 = right
        y_2 = bottom
    else:
        raise ValueError("Ye gadds! This codepath is impossible!")

    logging.getLogger(__name__).debug(
        f"Cropping image {image.filename}: old {right}x{bottom}; new {width}x{height}; upper-left anchor ({x_1}, {y_1}); lower-right anchor ({x_2}, {y_2})"
    )

    return image.crop((x_1, y_1, x_2, y_2))


def black_and_white(
    image: Image.Image, config: configuration.ManipConfig
) -> Image.Image:
    """Convert an image to full-depth black and white"""
    logger = logging.getLogger(__name__)
    logger.debug(f"Converting image {image.filename} to black and white")
    return image.convert("L")
