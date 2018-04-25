"""text/tag extraction helpers."""
import re


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
