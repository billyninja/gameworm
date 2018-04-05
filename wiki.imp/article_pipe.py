import re
from constants import ArticleOutcome as Ao
from store import (ArticleInfo, GameInfoCore, GameInfoAuthor, GameInfoCompany, GameInfoEngine, GameInfoRelease,
                   insert_article_info, insert_game_info)


def outer_peel(content):
    final_title = None

    try:
        pages = content["query"]["pages"]
    except KeyError:
        return -1, final_title, None, None

    for wpi, pg in pages.items():
        wpi = int(wpi)
        if int(wpi) == -1:
            return wpi, final_title, None, None

        rev = pg["revisions"][0]["*"]
        final_title = pg["title"]
        redir = bool(re.match("#REDIRECT", rev, flags=re.I))
        if redir:
            redir_title = rev.split("[[", 1)[1].split("]]")[0].strip()

            return "REDIR", redir_title, None, None

    # TODO, get to infobox
    # TODO, get infobox_subject
    import pdb; pdb.set_trace()

    return wpi, final_title, 2, 3


def inner_peel():
    return


def check_assertiveness():
    return


def get_uat_pointer():
    return


def game_info_prepare(gi_dict):
    GameInfoCore()
    GameInfoAuthor()
    GameInfoCompany()
    GameInfoEngine()
    GameInfoRelease()

    return


def open_article(conn, src_title, src_platform_slug, is_redir=False):
    src_title = re.sub("[\[\[]|[\]\]]", "", src_title)

    content = conn.fetch(src_title)
    assertive_info_hits = 0
    did_redir = False

    wpi, final_title, ib_subject, ib_meat = outer_peel(content)
    if wpi == -1:
        return Ao.FOUND_NOT, None, None, assertive_info_hits

    did_redir = wpi == "REDIR"
    if wpi == "REDIR":
        content = conn.fetch(final_title)
        wpi, final_title, ib_subject, ib_meat = outer_peel(content)

    # MOCK
    return Ao.FOUND_ASSERTIVE, did_redir, None, 5

    uat_type = check_assertiveness(final_title, ib_subject)
    if uat_type:
        uat_pointer = get_uat_pointer(final_title, content)

    # AT THIS POINT, ABLE TO INSTANTIATE: ArticleInfo
    ai = ArticleInfo(src_title, final_title, uat_type, uat_pointer)
    insert_article_info(ai)
    if uat_type:
        return Ao.FOUND_UAT, did_redir, uat_type, assertive_info_hits

    game_info_dict, assertive_info_hits = inner_peel(wpi, final_title, ib_subject, ib_meat)
    gi_core, authors, companies, engines, releases = game_info_prepare(game_info_dict)
    insert_game_info(gi_core, authors, companies, engines, releases)

    return Ao.FOUND_ASSERTIVE, did_redir, uat_type, assertive_info_hits
