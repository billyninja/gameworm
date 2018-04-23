import os
import json
from tag_match import _clean_entry
from gameworm import tty_colors as colors
from gameworm import file_storage


def _trim_plat_slug(plat):
    plat_slug = plat.strip().replace(" ", "_").lower()
    if "list_of_" in plat_slug:
        plat_slug = plat_slug.split("list_of_", 1)[1].split("_games")[0].strip()
    elif "index_of_" in plat_slug:
        plat_slug = plat_slug.split("index_of_", 1)[1].split("_games")[0].strip()

    return plat_slug


def extract_from_table(working_set, content, title):
    tables = content.split("{|")[1:]

    print("%d tables in %s\n" % (len(tables), title))
    for tb in tables:
        tb = tb.split("|}")[0]
        rows = tb.split("|-\n|")
        print(len(rows), "rows!")
        for rr in rows:
            rr = rr.replace('\n', '')
            try:
                raw_title = rr.split("|")[0]
                clean = _clean_entry(raw_title)
                if not clean:
                    continue

                working_set["set"].append(clean)
            except IndexError:
                continue


def extract_from_list(working_set, content, title):
    # TODO, understand list markup properly!
    # TODO, understand list markup properly!
    # TODO, understand list markup properly!
    # TODO, understand list markup properly!
    print("# TODO, understand list markup properly!")
    print("# TODO, understand list markup properly!")
    print("# TODO, understand list markup properly!")
    spl = content.split("\n*")
    # .split("|\'\'")
    print(title)
    print(len(spl))
    if len(spl) < 20:
        import pdb; pdb.set_trace()
    print("====")
    for entry in spl:
        if ("List of" in entry) or ("Lists of" in entry) or ("Category:" in entry):
            continue

        entry = entry.split("]]", 1)[0]
        clean = _clean_entry(entry)
        if not clean:
            continue
        working_set["set"].append(clean)


def parse_revision_content(partials_path, plat, content):
    platform_set = {
        "title": plat,
        "set": [],
    }

    if 'class="wikitable' in content:
        extract_from_table(platform_set, content, plat)
    else:
        extract_from_list(platform_set, content, plat)

    file_storage.store_partial(partials_path, plat, json.dumps(platform_set))
    return


def join_partials(partials_path):
    all_titles = []
    for entry in os.listdir(partials_path):
        fpath = os.path.join(partials_path, entry)
        if not (os.path.isfile(fpath) and entry.endswith(".json")):
            print("skipping %s" % entry)
            continue

        fh = open(fpath, "r")
        fcontent = fh.read()
        data = json.loads(fcontent)
        plat_slug = _trim_plat_slug(data["title"])
        for ss in data["set"]:
            all_titles.append((ss, plat_slug))

    all_titles = list(set(all_titles))

    fname = "all_titles__ct_%d" % len(all_titles)
    fname = os.path.join(partials_path, fname)

    fh = open(fname, "w+")
    fh.write(json.dumps(all_titles))
    fh.flush()
    fh.close()

    return all_titles, fname


def open_listings(conn, partials_path, desired_platforms):

    for plat in desired_platforms:
        try:
            resp = conn.fetch(plat)
        except Exception as e:
            print(e)
            continue

        # it is a loop but just to get the first
        for k, pg in resp["query"]["pages"].items():
            try:
                parse_revision_content(partials_path, plat, pg["revisions"][0]["*"])
            except Exception as e:
                print(colors.danger(e, True))
                break

    all_titles, all_titles_path = join_partials(partials_path)

    return all_titles, all_titles_path
