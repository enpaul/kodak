"""Application exceptions

::

  FresnelException
   +-- ClientError
   +-- ServerError
"""


class FresnelException(Exception):
    """Whomp whomp, something went wrong

    But seriously, don't ever raise this exception
    """

    status: int


class ClientError(FresnelException):
    """Error while processing client side input"""

    status = 400


class ImageResourceDeletedError(ClientError):
    """Requested image resource has been deleted"""

    status = 410


class ServerError(FresnelException):
    """Error while processing server side data"""

    status = 500


class ImageFileRemovedError(ServerError):
    """Image file removed from server"""
