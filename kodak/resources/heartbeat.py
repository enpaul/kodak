from kodak import configuration
from kodak import database
from kodak.resources._shared import KodakResource
from kodak.resources._shared import ResponseTuple


class Heartbeat(KodakResource):

    routes = ("/heartbeat",)

    def get(self) -> ResponseTuple:
        configuration.load()
        database.ImageRecord.select().count()

        return self.make_response(None)

    def head(self) -> ResponseTuple:
        return self._head(self.get())
