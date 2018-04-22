"""
Stage of the pipeline responsible for collecting and parsing a game article from the wikipedia.

    1) open a article
    2) preliminar parse, findout out:
        2.1) has a #REDIRECT directive in the response.
        2.2) the article subject.
        2.3) if it is assertive, ambigous, wrong etc.
    3) further extract useful/stadarized data from the revision content.
    4) insert in the DB.
"""

import re
from tag_match import tag_match, _infobox_pre_clean, _clean_entry, drop_none, _ref_strip, yolo_spl
from constants import UnassertiveArticle
from constants import ArticleOutcome as Ao
from store import (ArticleInfo, GameInfoCore, GameInfoAuthor, GameInfoCompany, GameInfoEngine, GameInfoRelease,
                   insert_article_info, insert_game_info)


samples = []


def outer_peel(content):

    try:
        pages = content["query"]["pages"]
    except KeyError:
        return -1, None

    for wpi, pg in pages.items():
        wpi = int(wpi)
        if int(wpi) == -1:
            return wpi, None

        rev = pg["revisions"][0]["*"]
        redir = bool(re.match("#REDIRECT", rev, flags=re.I))
        if redir:
            redir_title = rev.split("[[", 1)[1].split("]]")[0].strip()

            return "REDIR", redir_title

    return wpi, rev


ASSERTIVE_SUBJECTS = ["video game", "video games", "vg", "cvg"]
CROSSMEDIA_SUBJECTS = ["media franchise", "animanga/header", "film", "television",
                       "toy", "character", "comics character", "game", "comic book title", "hollywood cartoon",
                       "comics character", "comics organization", "lego theme", "comics meta series",
                       "wrestling promotion"]
GAME_SERIES_SUBJECTS = ["video game series", "video games series", "vg series", "video game character"]


def check_assertiveness(title, subject):
    print(subject)
    if not subject:
        return UnassertiveArticle.NO_INFOBOX_ARTICLE

    if subject in ASSERTIVE_SUBJECTS:
        return None

    if subject in GAME_SERIES_SUBJECTS:
        return UnassertiveArticle.GAME_SERIES_ARTICLE

    if subject in CROSSMEDIA_SUBJECTS:
        return UnassertiveArticle.CROSS_MEDIA_ARTICLE

    if subject in ["company", "person", "dot-com company", "aircraft begin", "software", "video game system",
                   "military conflict", "occupation", "settlement", "vg online service", "information appliance"]:
        return UnassertiveArticle.CONFIRMED_BAD_LEAD

    return UnassertiveArticle.WRONG_ARTICLE  # should try desambig.


def get_uat_pointer(a, b):
    return


def game_info_prepare(gi_dict):
    GameInfoCore()
    GameInfoAuthor()
    GameInfoCompany()
    GameInfoEngine()
    GameInfoRelease()

    return


def extract_infobox(rev):
    infobox_meat = subj = None
    try:
        infobox_meat = tag_match(rev, "infobox")
    except Exception as ex:
        print(ex)
        import pdb; pdb.set_trace()
    if infobox_meat:
        subj = infobox_meat.split("{{INFOBOX")[1].split("|")[0]
        subj = re.sub('\\n', '', subj).strip().lower()
        subj = subj.split("<!--")[0].strip()
    else:
        print("NO INFOBOX!!!")

    return subj, infobox_meat


def extract_desambig(title, rev):
    return False


def open_article(conn, src_title, src_platform_slug, is_redir=False):
    src_title = re.sub("[\[\[]|[\]\]]", "", src_title)
    src_title = src_title.replace("&", "%26")
    src_title = src_title.split("|")[0]
    final_title = src_title

    if ", The''" in final_title:
        final_title = final_title.split(", The''")[1]

    if "''" in final_title:
        final_title = final_title.split("''")[0]

    if '•' in final_title:
        final_title = final_title.strip('•')

    content = conn.fetch(final_title)
    assertive_info_hits = 0
    did_redir = False

    wpi, rev_content = outer_peel(content)
    if wpi == -1 or not rev_content:
        return Ao.FOUND_NOT, None, None, assertive_info_hits

    did_redir = wpi == "REDIR"
    if wpi == "REDIR":
        content = conn.fetch(rev_content)
        final_title = rev_content
        wpi, rev_content = outer_peel(content)
        if wpi == -1 or not rev_content:
            return Ao.FOUND_NOT, None, None, assertive_info_hits

    ib_subject, ib_meat = extract_infobox(rev_content)

    uat_type = check_assertiveness(final_title, ib_subject)
    if uat_type in [UnassertiveArticle.CROSS_MEDIA_ARTICLE, UnassertiveArticle.GAME_SERIES_ARTICLE]:
        uat_pointer = get_uat_pointer(final_title, content)
        # TEMP
        return Ao.FOUND_UAT, did_redir, None, 5
    elif uat_type is UnassertiveArticle.WRONG_ARTICLE:
        desambig = extract_desambig(final_title, rev_content)
        print("DESAMBIGUATION FOUND!!", desambig)
    elif uat_type is UnassertiveArticle.CONFIRMED_BAD_LEAD:
        return Ao.FOUND_NOT, did_redir, None, None
    elif not ib_meat:
        return Ao.NO_INFOBOX_ARTICLE, did_redir, None, None

    ib_clean_meat = _infobox_pre_clean(ib_meat)
    cti = inner_peel(ib_clean_meat)
    if "released" in cti:
        # if cti["released"] == "{{Collapsible list":
        #     import pdb; pdb.set_trace()

        vals = _ref_strip(cti["released"])

        # def _extract(v1, name="$VGrelease"):
        #     expr = "{{%s" % name
        #     spl = v1.split(expr)
        #     if len(spl) <= 1:
        #         return v1
        #     arr = []
        #     for ss in spl[1:]:
        #         arr.append(ss.split("}}")[0])

        #     return arr

        # def _extract_plats(v2):
        #     spl = v2.split("'''")
        #     arr2 = []
        #     for i, sp in enumerate(spl):
        #         if i % 2:
        #             arr2.append(sp)
        #     return arr2
        print(":::::", cti["released"])
        v1 = re.sub('id=\"|data-sort-value=\"|{{CITE WEB|<[^<]+?>', '§', vals, flags=re.I)
        v1 = re.sub("{{ vg|{{vg|{{Video\sgame\s", "{{$VG", v1, flags=re.I)
        exp1 = "'''|',|\{\{\$VGrelease|\}\}|§,\s|§§|<br?\\>|''|{{\$VGy\||\n"
        exp2 = "{{\s?Collapsible\slist\s?\|?(\stitle\s=\s[.]+\s\|)?"
        v2 = re.sub(exp1, "§", v1)
        v3 = re.sub(exp1, "§", v2)
        v4 = re.sub(exp2, "§", v3)
        if "§" in v3:
            spl = v3.split("§")
            if v3.startswith("{{"):
                spl = spl[1:]
            parts = [y for y in filter(lambda x: len(x) > 0 and x not in ["", "\n* ", "\n"], spl)]
            v4 = "§".join(parts)

        v4 = re.sub(exp1, "§", v4)
        def _acceptable(xpto):
            if xpto in ["{{collapsible list", ""]:
                return False
            return True
        accepted = False
        for vv in [v4, v3, v2, v1, vals]:
            if not _acceptable(vv):
                continue
            else:
                accepted = True
                v4 = vv
                break

        if not accepted:
            v4 = "<FB>" + cti["released"]
        samples.append(v4)

    # MOCK
    return Ao.FOUND_ASSERTIVE, did_redir, None, 5

    # AT THIS POINT, ABLE TO INSTANTIATE: ArticleInfo
    ai = ArticleInfo(src_title, final_title, uat_type, uat_pointer)
    insert_article_info(ai)
    if uat_type:
        return Ao.FOUND_UAT, did_redir, uat_type, assertive_info_hits

    game_info_dict, assertive_info_hits = inner_peel(wpi, final_title, ib_subject, ib_meat)
    gi_core, authors, companies, engines, releases = game_info_prepare(game_info_dict)
    insert_game_info(gi_core, authors, companies, engines, releases)


def release_breakdown(val):
    plats = val.split("<br>")
    import pdb; pdb.set_trace()