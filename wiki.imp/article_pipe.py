import re
from tag_match import tag_match
from constants import UnassertiveArticle
from constants import ArticleOutcome as Ao
from store import (ArticleInfo, GameInfoCore, GameInfoAuthor, GameInfoCompany, GameInfoEngine, GameInfoRelease,
                   insert_article_info, insert_game_info)


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


def inner_peel():
    return


ASSERTIVE_SUBJECTS = ["video game", "video games", "vg", "cvg"]
CROSSMEDIA_SUBJECTS = ["media franchise", "animanga/header", "film", "television",
                       "toy", "character", "comics character", "game", "comic book title",
                       "comics character", "comics organization", "lego theme"]
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

    if subject in ["company", "person", "dot-com company", "aircraft begin", "software", "video game system"]:
        return UnassertiveArticle.CONFIRMED_BAD_LEAD

    import pdb; pdb.set_trace()
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
        import pdb; pdb.set_trace()
    if infobox_meat:
        subj = infobox_meat.split("{{INFOBOX")[1].split("|")[0]
        subj = re.sub('\\n', '', subj).strip().lower()
        subj = subj.split("<!--")[0].strip()
    else:
        print("NO INFOBOX!!!")

    return subj, infobox_meat


def extract_desambig(title, rev):
    import pdb; pdb.set_trace()
    return False


def open_article(conn, src_title, src_platform_slug, is_redir=False):
    src_title = re.sub("[\[\[]|[\]\]]", "", src_title)
    src_title = src_title.replace("&", "%26")
    src_title = src_title.split("|")[0]
    final_title = src_title

    content = conn.fetch(src_title)
    assertive_info_hits = 0
    did_redir = False

    wpi, rev_content = outer_peel(content)
    if wpi == -1:
        return Ao.FOUND_NOT, None, None, assertive_info_hits

    did_redir = wpi == "REDIR"
    if wpi == "REDIR":
        content = conn.fetch(rev_content)
        final_title = rev_content
        wpi, rev_content = outer_peel(content)

    ib_subject, ib_meat = extract_infobox(rev_content)

    uat_type = check_assertiveness(final_title, ib_subject)
    if uat_type in [UnassertiveArticle.CROSS_MEDIA_ARTICLE, UnassertiveArticle.GAME_SERIES_ARTICLE]:
        uat_pointer = get_uat_pointer(final_title, content)
    elif uat_type is UnassertiveArticle.WRONG_ARTICLE:
        desambig = extract_desambig(final_title, rev_content)
        print("DESAMBIGUATION FOUND!!", desambig)
    elif uat_type is UnassertiveArticle.CONFIRMED_BAD_LEAD:
        return Ao.FOUND_NOT, did_redir, None, None

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

    return Ao.FOUND_ASSERTIVE, did_redir, uat_type, assertive_info_hits
