"""Core methods for find-data extraction/parsing."""
import os
import sys
import re
import json
from datetime import date, datetime
from normalization import author_role
from cons_platforms import PLATFORM_ALIASES
from region_tree import search_region_tree
from tag_match import tag_match, yolo_spl, _clean_entry, drop_none
from store import (ArticleInfo, GameInfoCore, GameInfoAuthor, GameInfoCompany,
                   GameInfoEngine, GameInfoRelease, GameInfoGenre, insert_game_info)
sys.path.append('../')
from gameworm import tty_colors

ASSERTIVE_SUBJECTS = ["video game", "video games", "vg", "cvg"]
CROSSMEDIA_SUBJECTS = ["media franchise", "animanga/header", "film", "television",
                       "toy", "character", "comics character", "game", "comic book title", "hollywood cartoon",
                       "comics character", "comics organization", "lego theme", "comics meta series",
                       "wrestling promotion"]
GAME_SERIES_SUBJECTS = ["video game series", "video games series", "vg series", "video game character"]


markup_rm = re.compile(",\s\[\[[0-9]{4}\sin\svideo\sgaming\||titlestyle")
markup_sep1 = re.compile("({{collapsible list\s?\|\s?(title=\s?[\w+\s,]+)?|\/|<[^<]+?>|{{\s?[A-Za-z]+\s?\||'''|''|\[\[|\]\]|}}|\\n|\s?=\s?([a-z\-]+:[a-z\s0-9]+(\;|\s\|))|{{\s?(vg|video game\s)release)", flags=re.I)
markup_sep2 = re.compile("\s?§\s?\|?§?\s?")
remove_date_commas = re.compile(
    "(\s[0-9]{1,2})?(Jan(uary)?|Feb(ruary)?|Mar(ch)|Apr(il)|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember))(\s[0-9]{1,2})?(?P<comma>\s?\,)"
)
special_date_pattern = re.compile(
    "((start|release)\s?date|dts|§)\|?([0-9]{4})\|([0-9]{1,2})\|([0-9]{1,2})")

special_date_pattern2 = re.compile(
    "(mid|late|early|q1|q2|q3|q4|fall|sprint|summer|winter|holidays)(-|\s)[0-9]{4}"
)

_isnoise = re.compile("\s?[\-\|\\|\[|\{|\}|\$|\%|\?|\.|,|url]\s?")


class Platform:

    def __init__(self, code, alias_used=None):
        if code not in PLATFORM_ALIASES.keys():
            code = find_plat_code(alias_used)
            if not code:
                raise ValueError("Not a known platform/platform-aliases: %s" % alias_used)

        self.alias_used = alias_used
        self.code = code

    def __repr__(self):
        return "<%s>" % self.code


class Region:

    def __init__(self, vl):
        self.vl = vl

    def __repr__(self):
        return "<%s>" % self.vl


def _is_region(inp):
    out = search_region_tree(inp)
    if out:
        return Region(out)

    return None


def _is_date(inp):
    if inp in ["TBA"]:
        return date(2099, 1, 1)

    patterns = [
        "%B %d %Y",
        "%B %Y",
        "%d %B %Y",
        "%d %b %Y",
        "%b %Y",
        "%Y-%m-%d",
        "%Y",
        "%B %dth %Y",
    ]

    for ptt in patterns:
        try:
            el = datetime.strptime(inp, ptt).date()
            if el.year < 1970 or el.year > 2022:
                raise ValueError("not a valid release year!")
            return el
        except ValueError:
            continue

    return None


def _repl_dt_comma(mo):
    if mo.group("comma"):
        span = mo.span()
        return mo.string[span[0]:span[1] - 1]


def _repl_special_dt(mo):
    span = mo.span()
    parts = mo.string[span[0] + 1:span[1] - 1].split("|")
    print(parts)
    p3 = 1

    try:
        p3 = int(parts[3])
        if p3 < 1 or p3 > 28:
            raise ValueError("going with a safe day range")
    except (ValueError, IndexError):
        p3 = 1
        pass

    dt = date(int(parts[1]), int(parts[2]), p3)

    return dt.strftime("|%B %d %Y")


def prenorm(inp):
    inp = markup_rm.sub(' ', inp)
    inp = markup_sep1.sub("§", inp)
    inp = markup_sep2.sub("§", inp)
    inp = markup_sep2.sub("§", inp)
    inp = inp.strip("§")
    inp = remove_date_commas.sub(_repl_dt_comma, inp)
    inp = special_date_pattern.sub(_repl_special_dt, inp)

    return inp

yf = re.compile("§|\||,|\sand\s|\(|\)\/")


def yank_forward(inp):

    if not yf.match(inp[-1]):
        inp += "§"

    values = []
    sk = 0
    last_yank = 0
    while sk < len(inp):
        mt = yf.match(inp[sk:])
        if mt:
            values.append(inp[last_yank:sk])
            last_yank = sk + 1
        sk += 1

    return values


def find_plat_code(alias):

    for code, aliases in PLATFORM_ALIASES.items():
        if alias == code:
            return code

        for al in aliases:
            if alias == al:
                return code

    return None


def is_plat(text):
    text = text.strip()
    code = find_plat_code(text)
    if code:
        return Platform(code, text)

    return None


def outer_peel(raw_content):
    wpi = None
    if isinstance(raw_content, dict):
        pass
    else:
        raw_content = json.loads(raw_content)

    for lvl in ["query", "pages", "$PID", "revisions", 0, "*"]:

        if lvl == "$PID":

            nk = len(raw_content)

            for k in raw_content.keys():

                wpi = k
                lvl = k
                if nk > 1:
                    if "game" in raw_content[k].get("title", "blank"):
                        break
                else:
                    break

        if isinstance(lvl, str) and (lvl not in raw_content):
            print(tty_colors.danger(lvl, " not in content dict"))
            return None, False

        raw_content = raw_content[lvl]

    return wpi, raw_content


def get_infobox(rev_content):
    si, sj = None, None
    for x in re.finditer("\{\{\s?Infobox", rev_content, flags=re.I):
        si, sj = x.span()
        break

    if si is None:
        print(tty_colors.danger("Infobox not found!"))
        return None, False

    slic = rev_content[si:]
    ib_subject = rev_content[sj + 1:].split("|", 1)[0]
    ib_subject = markup_sep1.sub("", ib_subject).strip()
    ib_content = tag_match(slic)

    return ib_subject, ib_content


def inner_peel(rev):
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
        "release": None,
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

    expected_info_fields = expected_values.keys()
    info_spl = yolo_spl(rev, "\n|")
    for chunk in info_spl[1:]:
        if "=" not in chunk:
            continue

        field, value = chunk.split("=", 1)
        field = _clean_entry(field).lower()

        if field in expected_info_fields:
            if field == "release":
                field = "released"

            expected_values[field] = value.strip()
            if len(expected_values[field]) > 0:
                field_hits += 1
        else:
            print("unexpected field: ", field, "with value: ", value)

    print("info hits: ", field_hits)
    return drop_none(expected_values)


def _generic_list_extraction(val):
    val = prenorm(val)
    val = re.sub('<[^<]+?>|\[|\]|http://.+|\(.+\)', '', val)
    return re.split("§|\||,|;", val)


def author_extraction(wpi, val, role):
    val2 = re.sub("<[^<]+?>|http://.+?(\||\])|\[|\]|\(.+\)", "§", val)
    val2 = set([x.strip().title() for x in re.split(",|§|;|\\n", val2)])
    out = []
    for val in val2:
        if len(val) > 5 and not re.findall("[^\w\s\.\']", val, flags=re.I):
            out.append(GameInfoAuthor(wpi, val, role))

    return out


def engine_extraction(wpi, val):
    values = list(set(re.findall("\[\[.+?\]\]", val)))
    return [GameInfoEngine(wpi, vv) for vv in values]


def mode_extraction(wpi, val):
    values = _generic_list_extraction(val)
    return values


def platform_extraction(wpi, val):
    values = list(set(re.findall("\[\[.+?\]\]", val)))
    out = []
    for vv in values:
        el = is_plat(vv)
        if el:
            out.append(el)

    return out


def genre_extraction(wpi, val):
    values = list(set(re.findall("\[\[.+?\]\]", val)))
    return [GameInfoGenre(wpi, vv) for vv in values]


def company_extraction(wpi, val, role):
    values = list(set(re.findall("\[\[.+?\]\]", val)))
    return [GameInfoCompany(wpi, re.sub("\#.+?\]", "", vv), role) for vv in values]


def id_sequence(sequence):
    prev = None
    out = []
    for x in sequence:
        if prev == x.__class__:
            continue
        out.append(x.__class__)
        prev = x.__class__

    if len(out) == 1 and out[0] is date:
        return "SIMPLE_DATE"
    elif len(out) > 2:
        if (out[0] is Platform and out[1] is Region and out[2] is date):
            return "P-R-D"
        elif (out[0] is Region and out[1] is date and out[2] is Platform):
            return "R-D-P"
        elif (out[0] is Region and out[1] is date and out[2] is not Platform):
            return "R-D"
        elif (out[0] is date and out[1] is Platform and out[2] is not Region):
            return "D-P"
        elif (out[0] is Platform and out[1] is Platform and out[2] is not Region):
            return "D-P"

    if len(out) >= 2 and (out[0] is Platform and out[1] is date):
        return "P-D"
    if len(out) >= 2 and (out[0] is Region and out[1] is date):
        return "R-D"

    return "UNK %d - %s" % (len(out), out)


def build_p_r_d(sequence):
    from copy import copy
    prev_plat = None
    out = []
    closed = False
    curr_sequence = []
    for idx, si in enumerate(sequence):

        if isinstance(si, Platform):
            if prev_plat == si.code:
                continue

            prev_plat = si.code
            if closed:
                out += copy(curr_sequence)
                curr_sequence = []
                closed = False

            curr_sequence.append(GameInfoRelease(si))

        if isinstance(si, Region):
            ow = False
            for ri in curr_sequence:
                if ri.region is None:
                    ri.region = si
                    ow = True

            if not ow:
                ext = []
                for rl in curr_sequence:
                    ext.append(GameInfoRelease(rl.platform, si))
                curr_sequence += ext

        if isinstance(si, date):
            for ri in curr_sequence:
                if ri.rdate is None:
                    ri.rdate = si
                    closed = True

    return out


def build_p_d(sequence):
    closed = False
    out = []
    for item in sequence:

        if isinstance(item, Platform):
            closed = False
            out.append(GameInfoRelease(item))

        if isinstance(item, date):
            closed = True
            for o in out:
                if not o.rdate:
                    o.rdate = item

    return out


def release_extraction(wpi, raw_val, platforms_fallback=[]):
    sequence = []
    inp = prenorm(raw_val)
    if len(inp) <= 1:
        return []

    vls = yank_forward(inp)
    for vv in vls:
        rg = pl = dt = None
        noise = bool(_isnoise.match(vv))
        if noise:
            continue

        rg = _is_region(vv)
        if rg:
            sequence.append(rg)
            continue

        pl = is_plat(vv)
        if pl:
            sequence.append(pl)
            continue

        dt = _is_date(vv)
        if dt:
            sequence.append(dt)

        # if noise:
        #     out = tty_colors.warning("NOISE", vv)
        # elif dt or rg or pl:
        #     out = tty_colors.success(vv, dt, rg, pl)
        # else:
        #     out = tty_colors.danger("UNRECOGNIZED", vv, dt, rg, pl)
        # print(out)

    sq_type = id_sequence(sequence)
    if sq_type == "R-D" and platforms_fallback:
        sequence = platforms_fallback + sequence
        sq_type = "P-R-D"

    if sq_type == "SIMPLE_DATE" and platforms_fallback:
        sequence = platforms_fallback + sequence
        sq_type = "P-D"

    if sq_type == "P-R-D":
        return build_p_r_d(sequence)
    if sq_type == "P-D":
        return build_p_d(sequence)
    else:
        if (not sequence or sequence[0] is None) and platforms_fallback:
            return release_last_effort(raw_val, platforms_fallback)

        print(sq_type)
        print(sq_type)
        print(sq_type)

        return release_last_effort(raw_val, platforms_fallback)

    return []


def release_last_effort(val, platforms):
    gr = None
    val = prenorm(val)
    dt = re.findall("[0-9]{4}", val)
    if not dt:
        return []

    dt = _is_date(dt[0])
    if not platforms:
        platforms = [Platform("FIXME")]

    gr = GameInfoRelease(platforms[0], rdate=dt)
    rg = re.findall("[A-Z]{2,3}", val)
    if rg:
        rg = _is_region(rg[0])
        gr.region = rg

    return [gr]


def _assertive_proc(src_title, wpi, ib_subject, inp):

    info_kv = inner_peel(inp)

    final_title, img, img_caption = None, None, None
    authors, game_releases, companies, engines, platforms, modes, genres = [], [], [], [], [], [], []
    if "platforms" in info_kv.keys():
        platforms = platform_extraction(wpi, info_kv["platforms"])

    for k, val in info_kv.items():
        if not val or len(val) == 1:
            print(tty_colors.warning("blank val for key %s" % k))
            continue

        if k == "title":
            final_title = val

        if k == "image":
            img = re.sub(r"File:|\[|\]|alt\=.+|Image:|\|.+", "", val)

        if k == "caption":
            img_caption = val

        auth_role = author_role(k)
        if auth_role[0]:
            authors += author_extraction(wpi, val, auth_role[1])

        if k in ["released", "release", "first release version", "first release date", "latest release version",
                 "latest release date", "year of inception", "first release"]:
            game_releases += release_extraction(wpi, val, platforms)

        if k in ["developer", "publisher"]:
            companies += company_extraction(wpi, val, k)

        if k in ["engine"]:
            engines += engine_extraction(wpi, val)

        if k in ["modes"]:
            modes += mode_extraction(wpi, val)

        if k in ["platform of origin"]:
            platforms += platform_extraction(wpi, info_kv["platforms"])

        if k in ["genre"]:
            genres += genre_extraction(wpi, val)

    if not final_title:
        final_title = src_title

    a_info = ArticleInfo(src_title, final_title, wpi, ib_subject, "MISSING-TODO", None, None)
    g_core = GameInfoCore(wpi, True, img, img_caption, genres, modes)
    t1 = datetime.now()
    insert_game_info(a_info, g_core, platforms=platforms, authors=authors, companies=companies, engines=engines, releases=game_releases)
    print(final_title, tty_colors.success((datetime.now() - t1).total_seconds()))

    return "SS"


def macro(conn, ent):

    ent = re.sub("\[\[|\]\]", '', ent).strip()
    resp_ct = conn.fetch(ent)

    wpi, rev = outer_peel(resp_ct)
    if not wpi or not rev:
        return "E1"

    should_redir = re.search("\#redirect", rev, flags=re.I)
    if should_redir:
        redir_to = re.findall("\[\[.+?\]\]", rev, flags=re.I)
        if redir_to:
            print(tty_colors.success("REDIR FROM: %s TO: %s." % (ent, redir_to[0])))
            return macro(conn, redir_to[0].strip("[").strip("]"))

    ib_subject, inp = get_infobox(rev)
    if not ib_subject or not inp:
        return "E2"

    ib_subject = ib_subject.lower()
    assertive = ib_subject in ASSERTIVE_SUBJECTS

    if assertive:
        return _assertive_proc(ent, wpi, ib_subject, inp)

    game_series = ib_subject in GAME_SERIES_SUBJECTS
    if game_series:
        return "VGS"

    cross = ib_subject in CROSSMEDIA_SUBJECTS
    if cross:
        print("TODO-CROSSMEDIA CONFIRMATION")
        return "CM"

    # skip_msg = tty_colors.danger("Skipping. Src Title: %s Subject: %s" % (ent, ib_subject))
    # print(skip_msg)
    return "E3"


if __name__ == "__main__":
    stats = {}
    ecount = 0
    raws_path = "/home/joao/projetos/gameworm/.data/wiki/raws/"
    for ent in os.listdir(raws_path):
        ecount += 1
        fpath = os.path.join(raws_path, ent)
        fh = open(fpath, "r")
        ct = fh.read()
        fh.close()
        t1 = datetime.now()
        out = macro(ent, ct)

        if out not in stats:
            stats.update({out: 1})
        else:
            stats[out] += 1
        print((datetime.now() - t1).total_seconds())
    print(ecount)
    print(stats)
