from typing import Tuple

from dehance.resources._shared import DehanceResource
from dehance.resources._shared import ResponseBody
from dehance.resources._shared import ResponseHeaders
from dehance.resources.image import Image
from dehance.resources.image import ImageUpload
from dehance.resources.openapi import OpenAPI
from dehance.resources.thumbnail import ThumbnailResize
from dehance.resources.thumbnail import ThumbnailScale


RESOURCES: Tuple[DehanceResource, ...] = (
    ImageUpload,
    Image,
    OpenAPI,
    ThumbnailScale,
    ThumbnailResize,
)
