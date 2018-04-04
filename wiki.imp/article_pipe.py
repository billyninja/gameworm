from constants import ArticleOutcome as Ao
from store import (ArticleInfo, GameInfoCore, GameInfoAuthor, GameInfoCompany, GameInfoEngine, GameInfoRelease,
                   insert_article_info, insert_game_info)


def outer_peel():
    return


def inner_peel():
    return


def check_assertiveness():
    return


def should_redir():
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
    content = conn.fetch()
    assertive_info_hits = 0

    should, redir = should_redir(content)
    if should:
        content = conn.fetch(redir)

    wpi, final_title, ib_subject, ib_meat = outer_peel(content)
    if wpi == -1:
        return Ao.FOUND_NOT, redir, None, assertive_info_hits

    uat_type = check_assertiveness(final_title, ib_subject)
    if uat_type:
        uat_pointer = get_uat_pointer(final_title, content)

    # AT THIS POINT, ABLE TO INSTANTIATE: ArticleInfo
    ai = ArticleInfo(src_title, final_title, uat_type, uat_pointer)
    insert_article_info(ai)
    if uat_type:
        return Ao.FOUND_UAT, redir, uat_type, assertive_info_hits

    game_info_dict, assertive_info_hits = inner_peel(wpi, final_title, ib_subject, ib_meat)
    gi_core, authors, companies, engines, releases = game_info_prepare(game_info_dict)
    insert_game_info(gi_core, authors, companies, engines, releases)

    return Ao.FOUND_ASSERTIVE, redir, uat_type, assertive_info_hits
