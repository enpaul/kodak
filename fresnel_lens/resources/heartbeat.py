from fresnel_lens import configuration
from fresnel_lens import database
from fresnel_lens.resources._shared import FresnelResource
from fresnel_lens.resources._shared import ResponseTuple


class Heartbeat(FresnelResource):

    routes = ("/heartbeat",)

    def get(self) -> ResponseTuple:
        configuration.load()
        database.ImageRecord.select().count()

        return self.make_response(None)

    def head(self) -> ResponseTuple:
        return self._head(self.get())
