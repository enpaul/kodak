from typing import Tuple

from fresnel_lens.resources._shared import FresnelResource
from fresnel_lens.resources._shared import ResponseBody
from fresnel_lens.resources._shared import ResponseHeaders
from fresnel_lens.resources.image import Image
from fresnel_lens.resources.image import ImageUpload
from fresnel_lens.resources.openapi import OpenAPI
from fresnel_lens.resources.thumbnail import ThumbnailResize
from fresnel_lens.resources.thumbnail import ThumbnailScale


RESOURCES: Tuple[FresnelResource, ...] = (
    ImageUpload,
    Image,
    OpenAPI,
    ThumbnailScale,
    ThumbnailResize,
)
