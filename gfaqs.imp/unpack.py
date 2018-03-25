import json


if __name__ == '__main__':
    gid_set = set()
    title_set = set()
    platform_set = set()

    fh = open("per_genre.json", "r")
    txt = fh.read()
    by_genre_base = json.loads(txt)
    for gnr in by_genre_base:
        for page in gnr[2]:
            for title in page:
                platform_set.add(title[0])
                gid_set.add(int(title[2]))
                title_set.add(title[3])

    platform_map = {k: [] for k in platform_set}
    title_map = {k: [] for k in title_set}
    for gnr in by_genre_base:
        for page in gnr[2]:
            for title in page:
                title_map[title[3]].append((title[0], int(title[2])))
                platform_map[title[0]].append(int(title[2]))

    versions_per_title = []
    for k, v in title_map.items():
        versions_per_title.append((k, len(v), [x[0] for x in v]))

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
