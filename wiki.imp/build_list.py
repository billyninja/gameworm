import os
import requests
import json
from constants import DESIRED_LISTS_SET
from datetime import datetime
import re

XPL = "https://en.wikipedia.org/w/api.php?format=json&" +\
      "action=query&prop=revisions&rvprop=content&titles=%s"

STORAGE_RAW = ".data/raws/"
STORAGE_PARTIALS = ".data/partials/"


def fetch(titles, section=None, persist_raw=True):
    rfilename = "wiki_raw_%s.json" % (titles.replace("/", "_"))
    rfilename = os.path.join(STORAGE_RAW, rfilename)

    if persist_raw and STORAGE_RAW and os.path.isfile(rfilename):
        print("from storage!")
        fh = open(rfilename, "r")
        text = fh.read()
        fh.close()
        return json.loads(text)

    furl = XPL % (titles)
    if section:
        furl += ("&rvsection=" + str(section))

    resp = requests.get(furl)
    if persist_raw and STORAGE_RAW:
        print("stored!")
        fh = open(rfilename, "w")
        fh.write(resp.text)
        fh.flush()
        fh.close()

    return json.loads(resp.text)


def extract_from_table(working_set, revision_content, title):
    tables = revision_content.split("{|")[1:]

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
                pass


def extract_from_list(working_set, revision_content, title):
    # TODO, understand list markup properly!
    # TODO, understand list markup properly!
    # TODO, understand list markup properly!
    # TODO, understand list markup properly!
    print("# TODO, understand list markup properly!")
    spl = revision_content.split("[[")
    for entry in spl:
        if ("List of" in entry) or ("Lists of" in entry) or ("Category:" in entry):
            continue
        entry = entry.split("]]", 1)[0]
        clean = _clean_entry(entry)
        if not clean:
            continue
        working_set["set"].append(clean)


def _clean_entry(entry):
    clean = re.sub(
        'id=\"|data-sort-value=\"|{{CITE WEB|<[^<]+?>|{{[^{{]+?}}',
        '', entry, flags=re.I
    ).strip().lstrip('\'').rstrip('\'')

    if len(clean) < 2 or ("class=" in clean) or ("style=" in clean) or clean.startswith("{{"):
        print(entry, clean)
        return None

    if "[[" in clean and "]]" not in clean:
        clean += "]]"

    if clean.endswith("\""):
        clean = clean[:-1]
    if "]]" in clean:
        clean = clean.split("]]")[0] + "]]"

    return clean


def parse_revision_content(storage, title, revision_content):

    platform_set = {
        "title": title,
        "set": [],
    }

    ftitle = re.sub("[\W]", "_", title)
    fname = "partial_%s.json" % (ftitle.lower())
    fh = open(os.path.join(storage, fname), "w")

    platform_set["set"] = list(set(platform_set["set"]))

    if 'class="wikitable' in revision_content:
        extract_from_table(platform_set, revision_content, title)
    else:
        extract_from_list(platform_set, revision_content, title)

    fh.write(json.dumps(platform_set))
    fh.flush()
    fh.close()


def prepare_storage():
    tm = datetime.now().strftime("%m%dT%H%M")
    path = os.path.join(STORAGE_PARTIALS, tm)

    if not os.path.isdir(path):
        pass
    else:
        path += "_2"

    os.mkdir(path)

    return path


def build_set():
    st_path = prepare_storage()

    for title in DESIRED_LISTS_SET:
        print("Entering %s...\n" % title)
        resp = fetch(title)
        # it is a loop but just to get the first
        for k, pg in resp["query"]["pages"].items():
            try:
                parse_revision_content(st_path, title, pg["revisions"][0]["*"])
            except Exception as e:
                print(d1(e))

    return st_path


def join_partials(st_path):
    all_titles = []
    for entry in os.listdir(st_path):
        fpath = os.path.join(st_path, entry)
        if not (os.path.isfile(fpath) and entry.endswith(".json")):
            print(w1("skipping %s" % entry))
            continue

        fh = open(fpath, "r")
        fcontent = fh.read()
        data = json.loads(fcontent)
        plat_slug = trim_plat_slug(data["title"])
        for ss in data["set"]:
            all_titles.append((ss, plat_slug))
        fh.close()

    all_titles = list(set(all_titles))
    tcount = len(all_titles)
    fh = open(os.path.join(st_path, "all__ct_%d.json" % (tcount)), "w")
    enc = json.dumps(all_titles)
    fh.write(enc)
    fh.flush()
    fh.close()

    return all_titles


def b1(ss):
    return "\033[1m\033[96m%s\033[0m --" % (ss)


def w1(ss):
    return "\033[1m\033[93m%s\033[0m --" % (ss)


def d1(ss):
    return "\033[1m\033[91m%s\033[0m --" % (ss)


def n1(ss):
    return "\033[1m\033[92m%s\033[0m --" % (ss)


def digest(rev):
    try:
        info_begin = rev.split("{{Infobox", 1)[1]
        print(b1(len(info_begin)))
    except:
        print(w1("no infobox! deal with it later!"))


def open_article(entry, plat_slug, prev_redir=False):
    ensured = "[[" in entry
    entry = re.sub("[\[\[]|[\]\]]", "", entry)
    resp = fetch(entry)
    hit = False
    clength = 0
    redir = False
    redir_title = ""
    for pid, content in resp["query"]["pages"].items():
        if int(pid) > 0:
            rev0 = content["revisions"][0]["*"]
            clength = len(rev0)
            hit = True
            redir = bool(re.match("#REDIRECT", rev0, flags=re.I))
            if redir:
                try:
                    redir_title = rev0.split("[[", 1)[1].split("]]")[0].strip()
                except Exception as e:
                    print(e)
            if prev_redir and clength > 300:
                print(b1("Redir - Success!"))

            if "may refer to:" in rev0:
                print(w1("ambiguous!"))
                poss = rev0.split("may refer to:", 1)[1].split("[[")
                for pos in poss:
                    if "video game" in pos.lower():
                        redir = True
                        redir_title = pos.split("]]", 1)[0]
                        print(n1("found desambiguation! -->"), redir_title)
                        break
    out = "%s Len:%d " % (entry, clength,)
    if hit and not redir:
        digest(rev0)
        out = b1(out)
    else:
        if ensured:
            out = d1(out)
        else:
            out = n1(out)
    print("[%s]" % plat_slug, out)

    if redir and redir_title and not prev_redir:
        print(w1("going in for redir!"))
        open_article(redir_title, plat_slug, entry)


def trim_plat_slug(plat):
    plat_slug = plat.strip().replace(" ", "_").lower()
    if "list_of_" in plat_slug:
        plat_slug = plat_slug.split("list_of_", 1)[1].split("_games")[0].strip()
    elif "index_of_" in plat_slug:
        plat_slug = plat_slug.split("index_of_", 1)[1].split("_games")[0].strip()
    return plat_slug


def crawl_in(all):
    for title, plat in all:
        plat_slug = trim_plat_slug(plat)
        open_article(title, plat_slug)

if __name__ == "__main__":
    st_path = build_set()
    all = join_partials(st_path)
    crawl_in(all)
