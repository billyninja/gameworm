"""text/tag extraction helpers."""
import re
from datetime import datetime, date
from cons_platforms import PLATFORM_ALIASES
from constants import REGIONS


def tag_match(text, tagname="infobox", op="{{", cl="}}"):
    # silly normalization
    # {{ infobox | {{ INFOBOX | {{InfoBox
    exp_out = "%s %s|%s%s" % (op, tagname, op, tagname)
    exp_in = "%s%s" % (op, tagname.upper())
    text = re.sub(exp_out, exp_in, text, 1, flags=re.I)

    spl = text.split(exp_in, 1)
    if len(spl) <= 1:
        return None

    text = exp_in + spl[1]
    opn = 0
    n = len(op)
    final_pos = 0
    for idx, _ in enumerate(text):
        slc = text[idx:idx + n]

        if slc == op:
            opn += 1
        elif slc == cl:
            opn -= 1

        if opn == 0:
            final_pos = idx + 2
            break

    return text[0:final_pos]


def ref_strip(xx):
    spl_ref = xx.split("<ref")
    clean = spl_ref[0]
    for sp in spl_ref[1:]:
        sp2 = sp.split("</ref>")
        if len(sp2) > 1:
            clean += "".join(sp2[1:])

    return clean


def tag_extract(text):
    extc = ("{{", "}}")
    n = 2

    acc = list()
    for idx, _ in enumerate(text):
        slc = text[idx:idx + n]

        extM0, extM1 = (slc == extc[0]), (slc == extc[1])

        if extM0:
            acc.append([idx, None])

        elif extM1:
            for aci in reversed(acc):
                if aci[1] is None:
                    aci[1] = (idx + 2)
                    break

    return acc


def xtrip(content):
    st = ref_strip(content.strip())
    ss = st.split("'''")
    acc = []
    if len(ss) > 1:
        ss = ss[1:]
        acc = []
        for idx, si in enumerate(ss):
            if idx % 2 == 0:
                acc.append([si, None])
            else:
                acc[-1][1] = si
    else:
        acc = _pre_clean(st)

    return acc


def drop_none(d):
    for k, v in dict(d).items():
        if v is None:
            del d[k]
    return d


def _infobox_pre_clean(ib_meat):
    ibc = re.sub('id=\"|data-sort-value=\"|{{CITE WEB|<[^<]+?>', '§', ib_meat, flags=re.I)
    ibc.replace("  ", " ")
    ibc = re.sub('\n\s\s?\||\|\n\s', '\n|', ib_meat)
    ibc = re.sub("\[http.+\]", " ", ibc)
    ibc = re.sub("titlestyle\s?\=.+[\||§]", " ", ibc)
    ibc = re.sub(
        "\{\{Collapsible\slist\|title\s?\=.+\||accessdate\s?\=.+§|{{\s?citation needed\s?\|\s?date\=",
        "§", ibc, flags=re.I
    )

    return ibc


def _ref_strip(val):
    arr = []
    val = re.sub("<ref|<\sref", "$OPT", val)
    val = re.sub("</ref>", "$CLT", val)
    spl = val.split("$OPT")
    if len(spl) <= 1:
        return val

    arr.append(spl[0])
    for p in spl[1:]:
        p2 = p.split("$CLT")
        if len(p2) > 1:
            arr.append(p2[1])

    return "".join(arr)


def _pre_clean(entry):
    return re.sub(
        'id=\"|data-sort-value=\"|{{CITE WEB|<[^<]+?>|{{[^{{]+?}}',
        '', entry, flags=re.I
    ).strip().lstrip('\'').rstrip('\'')


def _clean_entry(entry):
    clean = _pre_clean(entry)

    if len(clean) < 2 or ("class=" in clean) or ("style=" in clean) or clean.startswith("{{"):
        print(entry, clean)
        return ""

    if "[[" in clean and "]]" not in clean:
        clean += "]]"

    if clean.endswith("\""):
        clean = clean[:-1]
    if "]]" in clean:
        clean = clean.split("]]")[0] + "]]"

    return clean


def yolo_spl(text, sp, depth=1, op="{{", cl="}}"):
    from copy import copy

    lvl = 0
    spl = []
    l_sp = len(sp)
    l_tg = len(op)

    for idx, _ in enumerate(text):

        tg_chunk = text[idx:idx + l_tg]

        if tg_chunk == op:
            lvl += 1
            continue

        if tg_chunk == cl:
            lvl -= 1
            continue

        if lvl > depth:
            continue

        sp_chunk = text[idx:idx + l_sp]
        if sp_chunk == sp:
            spl.append(idx + l_sp)

    out = []
    spl2 = copy(spl)
    for ss in spl2:
        spl.append(ss - l_sp)

    spl.sort()
    last = len(spl) - 1

    skip_next = False
    for i, ss in enumerate(spl):
        if i == 0:
            out.append(text[:ss])
            continue

        if i == last:
            out.append(text[ss:])
            continue

        if skip_next:
            skip_next = False
            continue

        out.append(text[ss:spl[i + 1]])
        skip_next = True

    return out


def _is_noise(inp):
    xx = inp.strip()
    return xx in ["", " ", "*", "\n", "Released", "{{dts", "excl.", "}",
                  "Original version", "cartridge", "-", "$CLT", "{{plainlist", "ndash", "{{Collapsible list", "{{Dts",
                  "version", "<FB>", "{{ubl"]


def _is_plat(inp):
    xx = inp.strip()
    for plt in PLATFORM_ALIASES.values():
        if xx in plt:
            return Platform(xx)

        xx2 = xx.lower()
        if "others" in xx2:
            return Platform("<OTHERS>")
        elif "8 bit" in xx2:
            return Platform("<CATCHALL: 8-BIT>")
        elif "16 bit" in xx2:
            return Platform("<CATCHALL: 16-BIT>")
        elif "ports" in xx2:
            return Platform("<CATCHALL: ports>")
        elif "re-released" in xx2:
            return Platform("<CATCHALL: re-released>")


def _is_date(inp):
    patterns = [
        "%Y-%m-%d",
        "%Y",
        "%B %d, %Y",
        "%d %B %Y",
        "%b %d, %Y",
        "%B %d %Y",
        "%B %Y",
        "%B, %Y",
        "%b %Y",
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


class Platform:

    def __init__(self, vl):
        self.vl = vl

    def __repr__(self):
        return "<%s>" % self.vl


class Region:

    def __init__(self, vl):
        self.vl = vl

    def __repr__(self):
        return "<%s>" % self.vl


def _is_region(inp):
    xx = inp.strip()
    if xx in REGIONS:
        return Region(xx)

    return None


def extract_sequence(inp):

    excl_markup_1 = "{{\s?Collapsible\slist\s?\|(\s?title\s?=\s?)"
    inp = re.sub(excl_markup_1, "", inp)

    excl_markup_2 = "accessdate\s?=(.)+[§|\$]"
    inp = re.sub(excl_markup_2, "", inp)

    excl_markup_3 = "titlestyle\s?=(.)+;"
    inp = re.sub(excl_markup_3, "", inp)

    excl_markup_4 = "\[\[[0-9]{4}\sin\svideo gaming\|"
    inp = re.sub(excl_markup_4, "", inp)

    pre_spl_parts = []
    date_pattern = "\{\{((start|release)\s?date|dts)\s?\|([0-9]{4})\|([0-9]{1,2})\|([0-9]{1,2})?"
    resp = re.findall(date_pattern, inp)
    if len(resp):
        print("dt hit!")
        pre_spl_parts.append(
            date(int(resp[0][2]), int(resp[0][3]), int(resp[0][4]) if resp[0][4] else 1))
        inp = re.sub(date_pattern, '', inp, flags=re.I)

    spl = re.split("§|\||\:|\[|\]|\(|\)|–|;|\sversion?", inp)
    sequence = []
    extracted_parts = []
    count = 0
    while count < len(spl):
        ss = spl[count]
        count += 1
        ss = ss.strip()
        ss = ss.strip("'")
        ss = ss.strip("*")
        ss = ss.strip(",")

        if _is_noise(ss):
            continue

        el = _is_date(ss)
        if el and isinstance(el, date):
            sequence.append(el)
            extracted_parts.append(ss)
            continue

        if ("," in ss and "Touch" not in ss) or ("/" in ss and ("Gen" not in ss or "Fami" not in ss)) or\
           ("&" in ss) or (" and " in ss):
            spl2 = re.split(",|/|\&|\sand\s", ss)
            print(spl2)
            spl = spl[:count - 1] + spl2 + spl[count:]
            ss = spl2[0]
            # rewinding
            count -= 1
            continue

        el = _is_plat(ss)
        if el and isinstance(el, Platform):
            sequence.append(el)
            continue

        el = _is_region(ss)
        if el and isinstance(el, Region):
            sequence.append(el)
            continue

        print("what is this?")
        print("what is this?")
        print("what is this?")
        print(ss)
        print("====")

    return sequence


class Release:

    def __init__(self, platform, region=None, rdate=None):
        self.platform = platform
        self.region = region
        self.rdate = rdate

    def __repr__(self):
        return "[%s, %s, %s]" % (self.platform.vl, self.region.vl, self.rdate.strftime("%B %d, %Y"))


if __name__ == "__main__":
    si = "{{ ASD REF:{{ QWE }} ZXC {{ asd 123}} {{ qwe {{ asd 123}} {{ qwe qwe}} qwe}} }}"
    slices = tag_extract(si)
    print(si)
    print(slices)
    for sli in slices:
        print(si[sli[0]:sli[1]])
