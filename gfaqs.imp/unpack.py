import os
import json
from constants import STORAGE_PARTIALS
import requests
from datetime import datetime


def base_join():
    fh = open("per_genre.json", "r")
    txt = fh.read()
    fh.close()
    by_genre_base = json.loads(txt)

    for partial in os.listdir(STORAGE_PARTIALS):
        subpath = os.path.join(STORAGE_PARTIALS, partial)
        print(subpath)
        if os.path.isfile(subpath):
            fh2 = open(subpath, "r")
            stxt = fh2.read()
            pc = json.loads(stxt)
            fh2.close()
            genre_code = pc[0][1]
            if genre_code in by_genre_base:
                print("update", genre_code, len(pc[0][2]))
                by_genre_base[genre_code] = pc[0][2]
            else:
                print("create", genre_code, len(pc[0][2]))
                by_genre_base.update({genre_code: pc[0][2]})

    fh = open("per_genre.json", "w")
    fh.write(json.dumps(by_genre_base))
    fh.close()

    return by_genre_base

if __name__ == '__main__':
    gid_set = set()
    title_set = set()
    platform_set = set()

    by_genre_base = base_join()

    for k, gnr in by_genre_base.items():
        for page in gnr:
            for title in page:
                platform_set.add(title[0])
                gid_set.add(int(title[2]))
                title_set.add(title[3])

    platform_map = {k: set() for k in platform_set}
    title_map = {k: {"releases": set(), "wikipedia_pid": None} for k in title_set}
    for k, gnr in by_genre_base.items():
        for page in gnr:
            for title in page:
                title_map[title[3]]["releases"].add((title[0], int(title[2])))
                platform_map[title[0]].add(int(title[2]))

    versions_per_title = []
    for k, v in title_map.items():
        versions_per_title.append((k, len(v["releases"]), [x[0] for x in v["releases"]]))

    versions_per_title = sorted(versions_per_title, key=lambda x: x[1])
    versions_per_title.reverse()
    for vs in versions_per_title[0:10]:
        print("%s (%d): %s" % (vs[0], vs[1], vs[2]))

    titles_per_platform = []
    for k, v in platform_map.items():
        titles_per_platform.append((k, len(v)))

    titles_per_platform = sorted(titles_per_platform, key=lambda x: x[1])
    titles_per_platform.reverse()
    for vs in titles_per_platform[0:10]:
        print("%s (%d)" % (vs[0], vs[1]))

    fname = "gambase.%s.txt" % datetime.now().strftime("%y%m%d%H%M")
    fh = open(fname, "a+")
    for vs in versions_per_title:
        slug = vs[0]
        final_url = WIKIP % slug
        resp = requests.get(final_url)
        qr = json.loads(resp.text)

        if "-1" in qr["query"]["pages"]:
            print("miss! %s " % (slug))
        else:
            print("hit! %s " % (slug))
            for k, pid in qr["query"]["pages"]:
                title_map[slug]["wikipedia_pid"] = pid
                extracts = pid
                break

            title_map[slug]["releases"] = list(title_map[slug]["releases"])
            file_content = "%s --- %s\n" % (slug, json.dumps(title_map[slug]))
            fh.write(file_content)
            fh.flush()
