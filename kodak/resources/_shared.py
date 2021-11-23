"""Shared resource base with common functionality"""
import logging
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Tuple
from typing import Union

import flask
import flask_restful

from kodak import __about__


ResponseBody = Optional[Union[Dict[str, Any], List[Dict[str, Any]], List[str]]]


ResponseHeaders = Dict[str, str]


def authenticated(func) -> Callable:
    """Decorator to wrap endpoints that need a client to authenticate to access

    .. note:: This function has no effect if ``config.private`` is set to ``False``
    """

    def _wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    # TODO: Implement this

    return _wrapper


class ResponseTuple(NamedTuple):
    """Namedtuple representing the format of a flask-restful response tuple

    :param body: Response body; must be comprised only of JSON-friendly primative types
    :param code: HTTP response code
    :param headers: Dictionary of headers
    """

    body: ResponseBody
    code: int
    headers: ResponseHeaders


class KodakResource(flask_restful.Resource):
    """Extension of the default :class:`flask_restful.Resource` class

    Add a couple of useful things to the default resource class:

    * Adds the :meth:`options` method to respond to HTTP OPTION requests
    * Adds the :meth:`_head` method as a stub helper for responding to HTTP HEAD requests
    * Adds the :meth:`make_response` method which handles response formatting boilerplate
    * Type hints the :attr:`routes` attribute for usage in subclasses
    * Adds an instance logger

    .. warning:: This class is a stub and should not be directly attached to an application

    :attribute routes: Tuple of route paths that this resource should handle; can be unpacked into
                      ``flask_restful.Api().add_route()``
    """

    routes: Tuple[str, ...]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)

    def options(
        self, *args, **kwargs  # pylint: disable=unused-argument
    ) -> ResponseTuple:
        """Implement HTTP ``OPTIONS`` support

        `Reference documentation <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/OPTIONS>`_
        """

        verbs = ",".join([verb.upper() for verb in flask.request.url_rule.methods])

        return self.make_response(None, 204, {"Allowed": verbs})

    def _head(self, response: ResponseTuple) -> ResponseTuple:
        """Wrapper to implement HTTP ``HEAD`` support

        `Reference documentation <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/HEAD>`_

        .. note:: The ``head`` method cannot be implemented directly as an alias of ``get`` because
                  that would require a uniform signature for ``get`` across all resources; or some
                  hacky nonsense that wouldn't be worth it. This stub instead lets child resources
                  implement ``head`` as a oneliner.
        """
        return self.make_response(None, response.code, response.headers)

    def make_response(  # pylint: disable=no-self-use
        self,
        data: ResponseBody,
        code: int = 200,
        headers: Optional[ResponseHeaders] = None,
    ):
        """Create a response tuple from the current context

        Helper function for generating defaults, parsing common data, and formatting the response.

        :param data: Response data to return from the request
        :param code: Response code to return; defaults to `200: Ok <https://httpstatuses.com/200>`_
        :param headers: Additional headers to return with the request; the default headers will
                        be added automatically and do not need to be passed.
        :returns: Response tuple ready to be returned out of a resource method

        .. note:: This function will handle pagination and header assembly internally. The response
                  data passed to the ``data`` parameter should be unpaginated.
        """

        headers = headers or {}
        headers.update({"Server": f"{__about__.__title__}-{__about__.__version__}"})

        # 204 code specifies that it must never include a response body. Most clients will ignore
        # any response body when a 204 is given, but that's no reason to abandon best practices here
        # on the server side
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/204
        return ResponseTuple(
            body=data if code != 204 else None, code=code, headers=headers
        )
