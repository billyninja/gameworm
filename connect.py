import json
import requests
from gameworm import file_storage


class Driver:

    def __init__(self, imp, raws):
        if imp != "wiki":
            raise NotImplementedError("Connection for %s not implemented!" % imp)

        self.imp = imp
        self.raws = raws
        self._base_url = "https://en.wikipedia.org/w/api.php?format=json&" +\
                         "action=query&prop=revisions&rvprop=content&titles=%s"

    def fetch(self, title, section=None, persist_raw=True):
        final_url = self._base_url % (title)

        if self.raws:
            resp = file_storage.fetch_from_raws(self.raws, title)
            if resp:
                return resp

        resp = requests.get(final_url).text

        if self.raws:
            file_storage.store_raw(self.raws, title, resp)

        return json.loads(resp)
