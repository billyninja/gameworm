import os
from time import sleep
import math
import json
from datetime import datetime
import requests
from constants import GENRES
from base64 import b64decode

BASE_URL = b"aF90X3RfcF9zXzpfL18vX2dfYV9tX2VfZl9hX3Ffc18uX2dfYV9tX2Vfc19wX29fdF8uX2Nfb19t"
BASE_URL = b64decode(BASE_URL).decode("ascii").replace("_", "")
PATH = "/games/rankings?platform=0&genre=%d&list_type=rate&view_type=0&dlc=0&min_votes=1&page=%d"
CRAWL_URL = "%s%s" % (BASE_URL, PATH)
PER_PAGE = 50
UA = {
    'User-agent':
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.33 Safari/537.36'
}

per_genre = []
PLATFORM_MAP = {}

STORAGE_PARTIALS = "/tmp/gameworm_data_partials"
STORAGE_RAW = "/tmp/gameworm_data_raw"


for st in [STORAGE_PARTIALS, STORAGE_RAW]:
    if not os.path.isdir(st):
        os.mkdir(st)


def fetch(page_count, persist_raw=False):
    final_url = CRAWL_URL % (code, page_count)
    t1 = datetime.now()
    resp = requests.get(final_url, headers=UA)
    print((datetime.now() - t1).total_seconds())

    if resp.status_code is not 200:
        raise Exception("CONNECTION ERROR!!! %s Received: %d - \n\n\n %s", final_url, resp.status_code, resp.text)

    if persist_raw and STORAGE_RAW:
        filename = "code_%d_page_%d.json" % (code, page_count)
        fh = open(os.path.join(STORAGE_RAW, filename), "w")
        fh.write(resp.text)
        fh.close()

    return resp.text

for name, code in GENRES:

    # TEMP lets not scrap by subgenre for now
    # TODO make it a proper setting
    if " >> " in name:
        continue

    genr_rank = (name, code, [])
    page_count = 0
    text = fetch(0, True)
    sleep(1)

    count = text.split('class="totalresults', 1)[1].split(">")[1].strip().split(" ")[0]
    total_page_count = math.ceil(int(count) / PER_PAGE)

    if code == 0:
        continue

    for pcount in range(total_page_count):
        t1 = datetime.now()

        if pcount > 0:
            text = fetch(pcount, True)
            sleep(1)

        try:
            core1 = text.split('<table class="results">', 1)[1].split("</table>", 1)[0]
        except IndexError as e:
            print(e)
            continue

        rows = core1.split("<tr>")

        for rw in rows:
            plat_abbr = title = title_slug = game_id = deeplink = None

            cols = rw.split("<td ")
            if not cols:
                continue

            for n, col in enumerate(cols):

                # Plaform
                if n == 2:
                    plat_abbr = col.split('class="rmain">', 1)[1].split("</td>")[0].strip()
                    if plat_abbr not in PLATFORM_MAP:
                        PLATFORM_MAP.update({plat_abbr: {"slug": None}})

                # Game Name And Link
                elif n == 3:
                    sspl = col.split('href="', 1)
                    deeplink = sspl[1].split('"')[0].strip()
                    dl_spl = deeplink.split("/")

                    # needless in the future
                    PLATFORM_MAP[plat_abbr]["slug"] = dl_spl[1].strip()
                    game_id, title_slug = dl_spl[2].split("-", 1)
                    print(game_id, title_slug)

                    title = sspl[1].split('">', 1)[1].split('</a>')[0]
                else:
                    # TODO, grab rating, difficulty and gameplay hours.
                    continue

            if not (plat_abbr or title or deeplink):
                continue

            genr_rank[2].append((plat_abbr, title, deeplink,))

        print((datetime.now() - t1).total_seconds())
        print(genr_rank)

    # -- finished walking through all pages!

    per_genre.append(genr_rank)
    "games_by_genre_partial.%s.json" % (name.replace(" >> ", "__"))
    partial_path = os.path.join(STORAGE_PARTIALS, )

    fh = open(partial_path, "w")
    fh.write(json.dumps(genr_rank))
    fh.close()

fh = open("per_genre.json", "w")
fh.write(json.dumps(per_genre))
fh.close()
