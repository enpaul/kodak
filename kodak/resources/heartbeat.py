from kodak import database
from kodak.resources._shared import KodakResource
from kodak.resources._shared import ResponseTuple


class Heartbeat(KodakResource):
    """Expose a heartbeat endpoint to check service health"""

    routes = ("/heartbeat",)

    def get(self) -> ResponseTuple:
        """Perform a trivial database operation and return a-ok"""
        database.ImageRecord.select().count()

        return self.make_response(None)

    def head(self) -> ResponseTuple:
        """Alias HEAD to GET"""
        return self._head(self.get())
