from typing import Tuple

from imagemonk.resources._shared import ImageMonkResource
from imagemonk.resources._shared import ResponseBody
from imagemonk.resources._shared import ResponseHeaders
from imagemonk.resources.image import Image
from imagemonk.resources.image import ImageUpload
from imagemonk.resources.openapi import OpenAPI
from imagemonk.resources.thumbnail import ThumbnailResize
from imagemonk.resources.thumbnail import ThumbnailScale


RESOURCES: Tuple[ImageMonkResource, ...] = (
    ImageUpload,
    Image,
    OpenAPI,
    ThumbnailScale,
    ThumbnailResize,
)
