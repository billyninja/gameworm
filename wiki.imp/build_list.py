import os
import requests
import json
from constants import DESIRED_LISTS_SET
from datetime import datetime
import re
from tag_match import tag_match, xtrip, _clean_entry, drop_none

XPL = "https://en.wikipedia.org/w/api.php?format=json&" +\
      "action=query&prop=revisions&rvprop=content&titles=%s"

STORAGE_RAW = ".data/raws/"
STORAGE_PARTIALS = ".data/partials/"


def section_finder(rev):
    for idx, subj in enumerate(re.finditer("=?=[\w ]+=?=", rev)):
        if re.findall('(game)|(video game)', subj.group()):
            return idx + 1

    return None


def fetch(titles, section=None, persist_raw=True):
    rfilename = "wiki_raw_%s.json" % (titles.replace("/", "_"))
    rfilename = os.path.join(STORAGE_RAW, rfilename)
    if len(rfilename) > 256:
        rfilename = "%s.json" % rfilename.split("''")[0]

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
                continue


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


def build_set(st_path):

    for title in DESIRED_LISTS_SET:
        print("Entering %s...\n" % title)

        try:
            resp = fetch(title)
        except Exception as e:
            print(e)
            continue

        # it is a loop but just to get the first
        for k, pg in resp["query"]["pages"].items():
            try:
                parse_revision_content(st_path, title, pg["revisions"][0]["*"])
            except Exception as e:
                print(d1(e))
                break

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
        plat_slug = _trim_plat_slug(data["title"])
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


expected_info_fields = ("title", "image", "developer", "publisher", "designer", "composer", "engine", "released")


def digest(rev):
    field_hits = 0
    expected_values = {
        "title": None,
        "image": None,
        "caption": None,
        "developer": None,
        "publisher": None,
        "designer": None,
        "composer": None,
        "engine": None,
        "released": None,
        "genre": None,
        "modes": None,
        "series": None,
        "director": None,
        "producer": None,
        "programmer": None,
        "artist": None,
        "writer": None,
        "platforms": None,
        "creator": None,
        "first release version": None,
        "first release date": None,
        "latest release version": None,
        "latest release date": None,
        "platform of origin": None,
        "year of inception": None,
        "spinoffs": None,
        "first release": None,
    }
    meta = {
        "is_series": False,
        "subject": False,
        "is_vg": False,
        "hybrid_article": False,
    }
    expected_info_fields = expected_values.keys()

    ipos = rev.find("{{Infobox")
    if ipos >= 0:
        info = tag_match(rev[ipos:])
        if "\n|" in info:
            info_spl = info.split("\n|")
        else:
            info_spl = info.split(" |")
        subject = info_spl[0].lower()
        meta["subject"] = subject
        meta["is_vg"] = ("game" in subject) or ("vg" in subject)
        meta["is_series"] = "series" in subject
        if not meta["is_vg"]:
            meta["is_vg"] = (("video game" in info) or ("==Video game" in rev) or ("== Video game" in rev))
            meta["hybrid_article"] = meta["is_vg"]
            sec = section_finder(rev)
            if sec:
                xx = fetch(title, section=sec)
            return drop_none(expected_values), meta

        for chunk in info_spl[1:]:
            if "=" not in chunk:
                continue

            field, value = chunk.split("=", 1)
            field = _clean_entry(field).lower()

            if field in expected_info_fields:
                expected_values[field] = xtrip(value)
                if len(value) > 0:
                    field_hits += 1
            else:
                print("unexpected field: ", field, "with value: ", value)
    else:
        print(w1("no infobox! deal with it later!"))
    print("info hits: ", field_hits)
    return drop_none(expected_values), meta


def open_article(entry, plat_slug, prev_redir=False):
    ensured = "[[" in entry
    entry = re.sub("[\[\[]|[\]\]]", "", entry)

    try:
        resp = fetch(entry)
    except Exception as e:
        print(d1(e))

    hit = False
    clength = 0
    redir = False
    redir_title = ""
    out_tty = ""

    if "query" not in resp:
        print(entry)
        print(d1("premature fail!! empty content!"))
        print(d1(resp))
        return None, resp

    if "pages" not in resp["query"]:
        print(entry)
        print(d1("premature fail!! empty content!"))
        print(d1(resp))
        return None, resp

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
    out_tty = "%s Len:%d " % (entry, clength,)
    if redir and redir_title and not prev_redir:
        print(w1("going in for redir!"))
        return open_article(redir_title, plat_slug, entry)

    if hit:
        info, meta = digest(rev0)

        if meta["is_series"]:
            out_tty += w1("-is series!-")

        if meta["is_vg"]:
            out_tty += b1("-is vg!-")
        else:
            out_tty += d1("IGNORE! NOT A GAME!!!")

        out_tty += b1(out_tty)
        print(out_tty)
        return info, meta
    else:
        if ensured:
            out_tty = d1(out_tty)
        else:
            out_tty = n1(out_tty)

    print(out_tty)
    return None, resp


def _trim_plat_slug(plat):
    plat_slug = plat.strip().replace(" ", "_").lower()
    if "list_of_" in plat_slug:
        plat_slug = plat_slug.split("list_of_", 1)[1].split("_games")[0].strip()
    elif "index_of_" in plat_slug:
        plat_slug = plat_slug.split("index_of_", 1)[1].split("_games")[0].strip()

    return plat_slug


def crawl_in(st_path, all):

    good = list()
    bad = list()
    for title, plat in all:
        plat_slug = _trim_plat_slug(plat)
        info, meta = open_article(title, plat_slug)
        if info and meta:
            good.append((title, info, meta,))
        else:
            bad.append((title, plat_slug, meta,))

    path = os.path.join(st_path, "good__ct_%d.json" % len(good))
    fh = open(path, "w")

    path = os.path.join(st_path, "bad__ct_%d.json" % len(bad))
    fh2 = open(path, "w")

    good_dump = json.dumps(good)
    fh.write(good_dump)
    fh.flush()
    fh.close()

    bad_dump = json.dumps(bad)
    fh2.write(bad_dump)
    fh2.flush()
    fh2.close()

    return len(good), len(good_dump), len(bad), len(bad_dump), len(all)

if __name__ == "__main__":
    st_path = prepare_storage()
    build_set(st_path)
    all = join_partials(st_path)
    g, gd, b, bd, al = crawl_in(st_path, all)
    x = 1024 * 1024
    out = "Good: %d (%2.fMB) // Bad: %d (%2.fMB) // all: %d" % (g, gd / x, b, bd / x, al)
    print(out)
