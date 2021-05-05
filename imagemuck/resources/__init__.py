from typing import Tuple

from imagemuck.resources._shared import ImageMuckResource
from imagemuck.resources._shared import ResponseBody
from imagemuck.resources._shared import ResponseHeaders
from imagemuck.resources.image import Image
from imagemuck.resources.image import ImageUpload
from imagemuck.resources.openapi import OpenAPI
from imagemuck.resources.thumbnail import ThumbnailResize
from imagemuck.resources.thumbnail import ThumbnailScale


RESOURCES: Tuple[ImageMuckResource, ...] = (
    ImageUpload,
    Image,
    OpenAPI,
    ThumbnailScale,
    ThumbnailResize,
)
