import sys
import os
from time import sleep
import math
import json
from datetime import datetime
import requests
from constants import GENRES, STORAGE_PARTIALS, STORAGE_RAW
from base64 import b64decode

BASE_URL = b"aF90X3RfcF9zXzpfL18vX2dfYV9tX2VfZl9hX3Ffc18uX2dfYV9tX2Vfc19wX29fdF8uX2Nfb19t"
BASE_URL = b64decode(BASE_URL).decode("ascii").replace("_", "")
PATH = "/games/rankings?platform=0&genre=%d&list_type=rate&view_type=0&dlc=0&min_votes=2&page=%d"
CRAWL_URL = "%s%s" % (BASE_URL, PATH)
PER_PAGE = 50
UA = {
    'User-agent':
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.33 Safari/537.36'
}

per_genre = []
PLATFORM_MAP = {}


def fetch(gcode, page_count, persist_raw=False):

    rfilename = "code_%d_page_%d.json" % (gcode, page_count)
    rfilename = os.path.join(STORAGE_RAW, rfilename)
    if persist_raw and STORAGE_RAW and os.path.isfile(rfilename):
        fh = open(rfilename, "r")
        text = fh.read()
        fh.close()
        return text, True

    final_url = CRAWL_URL % (gcode, page_count)
    t1 = datetime.now()
    resp = requests.get(final_url, headers=UA)
    print((datetime.now() - t1).total_seconds())

    if resp.status_code is not 200:
        raise Exception("CONNECTION ERROR!!! %s Received: %d - \n\n\n %s", final_url, resp.status_code, resp.text)

    if persist_raw and STORAGE_RAW:
        fh = open(rfilename, "w")
        fh.write(resp.text)
        fh.close()

    return resp.text, False


def check_storage():
    for st in [STORAGE_PARTIALS, STORAGE_RAW]:
        if not os.path.isdir(st):
            os.mkdir(st)

    presented_partials = []
    for partial in os.listdir(STORAGE_PARTIALS):
        spl = partial.split("games_by_genre_partial.", 1)
        if len(spl) > 1:
            gname = spl[1].split(".json", 1)[0]
            for gn in GENRES:
                if gname == gn[0]:
                    presented_partials.append(gn[1])

    return presented_partials


def parse_rank_table(text, code, pcount):
    resp = []

    try:
        core1 = text.split('<table class="results">', 1)[1].split("</table>", 1)[0]
    except IndexError:
        return

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
        resp.append((plat_abbr, title, game_id, title_slug, deeplink,))

    return resp


def run(included=[], excluded=[]):
    for name, code in GENRES:

        # TEMP lets not scrap by subgenre for now
        # TODO make it a proper arg/setting
        if (" >> " in name) or (excluded and code in excluded) or (included and code not in included):
            continue
        genr_rank = (name, code, [])
        text, local = fetch(code, 0, True)
        sleep(3)

        count = text.split('class="totalresults', 1)[1].split(">")[1].strip().split(" ")[0]
        total_page_count = int(math.ceil(int(count) / PER_PAGE))

        for pcount in range(total_page_count):
            if pcount > 0:
                text, local = fetch(code, pcount, True)
                tt = parse_rank_table(text, code, pcount)
                genr_rank[2].append(tt)
                if not local:
                    sleep(3)

        per_genre.append(genr_rank)
        filename = "games_by_genre_partial.%s.json" % (name.replace(" >> ", "__"))
        partial_path = os.path.join(STORAGE_PARTIALS, filename)

        fh = open(partial_path, "w")
        fh.write(json.dumps(per_genre))
        fh.close()

    fh = open("per_genre.json", "w")
    fh.write(json.dumps(per_genre))
    fh.close()


def proc_args():
    included, excluded = [], []

    for ag in sys.argv[1:]:
        if ag.startswith("-I"):
            for ex in ag.split("-I=")[1].split(","):
                included.append(int(ex))

        if ag.startswith("-X"):
            for ex in ag.split("-X=")[1].split(","):
                excluded.append(int(ex))

    return (included, excluded,)


if __name__ == '__main__':
    included, excluded, = proc_args()
    partials = check_storage()
    excluded += partials
    excluded += [0]  # just ensuring it wont try to parse 0 (all games at once)
    # ct, local = fetch(54, 0, True)
    # tt = parse_rank_table(ct, 54, 0)

    run(included, excluded)
