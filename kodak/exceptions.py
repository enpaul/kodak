"""Application exceptions

::

  KodakException
   +-- ClientError
   +-- ServerError
"""


class KodakException(Exception):
    """Whomp whomp, something went wrong

    But seriously, don't ever raise this exception
    """

    status: int


class ClientError(KodakException):
    """Error while processing client side input"""

    status = 400


class ImageResourceDeletedError(ClientError):
    """Requested image resource has been deleted"""

    status = 410


class IAmATeapotError(ClientError):
    """User tried to brew coffee, but application is a teapot"""

    status = 418


class ServerError(KodakException):
    """Error while processing server side data"""

    status = 500


class ImageFileRemovedError(ServerError):
    """Image file removed from server"""


class ConfigurationError(ServerError):
    """Failed to load the application configuration"""
