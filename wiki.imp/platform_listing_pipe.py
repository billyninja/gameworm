import tty_colors as colors
import storage
import json
from tag_match import _clean_entry


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
    spl = content.split("[[")
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

    storage.store_partial(partials_path, plat, json.dumps(platform_set))
    return


def open_listings(conn, all_titles_path, desired_platforms):

    for plat in desired_platforms:
        print("Entering %s...\n" % plat)

        try:
            resp = conn.fetch(plat)
        except Exception as e:
            print(e)
            continue

        # it is a loop but just to get the first
        for k, pg in resp["query"]["pages"].items():
            try:
                parse_revision_content(all_titles_path, plat, pg["revisions"][0]["*"])
            except Exception as e:
                print(colors.danger(e, True))
                break

    return all_titles_path
