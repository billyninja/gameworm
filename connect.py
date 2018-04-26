import json
import requests
from gameworm import file_storage


class Driver:

    def __init__(self, imp, raws, work_offline=False):
        if imp != "wiki":
            raise NotImplementedError("Connection for %s not implemented!" % imp)

        self.imp = imp
        self.raws = raws
        self._base_url = "https://en.wikipedia.org/w/api.php?format=json&" +\
                         "action=query&prop=revisions&rvprop=content&titles=%s"
        self.work_offline = work_offline

        if self.work_offline and not self.raws:
            raise ValueError("Cant work offline if RAWS is not filled!")

    def fetch(self, title, section=None, persist_raw=True):
        title = title.replace("&", "%26")
        final_url = self._base_url % (title)

        if self.raws:
            resp = file_storage.fetch_from_raws(self.raws, title)
            if resp:
                return resp

            if self.work_offline:
                return {}

        print("-/-", title)
        resp = requests.get(final_url).text

        if self.raws:
            file_storage.store_raw(self.raws, title, resp)

        try:
            return json.loads(resp)
        except Exception as e:
            print(resp)
            import pdb; pdb.set_trace()
