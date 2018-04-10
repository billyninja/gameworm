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


if __name__ == "__main__":
    si = "{{ ASD REF:{{ QWE }} ZXC {{ asd 123}} {{ qwe {{ asd 123}} {{ qwe qwe}} qwe}} }}"
    slices = tag_extract(si)
    print(si)
    print(slices)
    for sli in slices:
        print(si[sli[0]:sli[1]])
    s2 = " {{collapsible list|title=July 14, 1983|'''Arcade'''{{vgrelease|JP|July 14, 1983<ref>{{cite web|url=https://www.youtube.com/watch?v=cntz1GyM1Bs|title=Nintendo Direct 2.14.2013|work=Nintendo YouTube|publisher=[[YouTube]]|date=2013-02-14|accessdate=2013-02-16}}</ref><ref>{{cite web |url=https://kotaku.com/happy-30th-birthday-to-video-gamings-most-famous-broth-779535652 |title=Happy 30th Birthday to Video Gaming's Most Famous Brother |last=Good |first=Owen |date=2013-07-14 |website=[[Kotaku]] |publisher=[[Gizmodo Media Group]] |access-date=2018-03-08}}</ref>|NA|July 20, 1983}}'''Famicom/NES'''{{vgrelease|JP|September 9, 1983|NA|June 20, 1986|EU|September 1, 1986}}<u>Mario Bros. (Classic Series)</u>{{Vgrelease|EU|1993}}'''Atari 2600'''{{vgrelease|NA|1983}}'''Atari 5200'''{{vgrelease|NA|1983}}'''PC-88'''{{vgrelease|JP|February 1984}}'''Apple II'''{{vgrelease|NA|1984}}'''FM-7'''{{vgrelease|JP|1984}}'''NEC PC88'''{{vgrelease|JP|1984}}'''Commodore 64'''{{vgrelease|NA|1986}}'''Amstrad CPC'''{{vgrelease|EU|1987}}'''ZX Spectrum'''{{vgrelease|EU|1987}}'''Atari 7800'''{{vgrelease|NA|1988}}'''Atari 8-Bit'''{{vgrelease|NA|1989}}'''Game Boy Advance'''<br> e-Reader{{vgrelease|NA|November 11, 2002}}Famicom Mini{{vgrelease|JP|May 21, 2004}}'''Virtual Console'''<br><u>Wii</u>{{vgrelease|NA|November 19, 2006}}{{vgrelease|PAL|December 8, 2006}}{{vgrelease|JP|December 12, 2006|Korea|KR|December 30, 2008}}<u>Nintendo 3DS</u>{{vgrelease|JP|May 8, 2013|EU|January 9, 2014|NA|January 30, 2014}}<u>Wii U</u>{{vgrelease|JP|May 29, 2013|WW|June 20, 2013}}'''Nintendo Switch'''{{vgrelease|WW|September 27,2017}}}}"
    xx = xtrip(s2)
