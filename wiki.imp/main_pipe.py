import sys
sys.path.append('../')

from constants import DESIRED_PLATFORMS, UAT_DISPLAY
from constants import ArticleOutcome as Ao, ARTICLE_OUTCOME_DISPLAY as AO_DISPLAY
from article_pipe import open_article
from platform_listing_pipe import open_listings
from gameworm import file_storage
from gameworm import tty_colors as colors
from gameworm.connect import Driver


def open_article_to_tty(title, outcome, did_redir, uat, hits):
    ao_tty_colors = {
        Ao.FOUND_ASSERTIVE: colors.success,
        Ao.FOUND_UAT: colors.warning,
        Ao.FOUND_NOT: colors.neutral_bland,
    }

    ao_display = AO_DISPLAY.get(outcome, "UNKNOW ARTICLE OUTCOME %d" % outcome)
    msg = ao_tty_colors[outcome](title + " - " + ao_display, bold=True)

    if did_redir:
        msg += " -> Redir" % bool(did_redir)

    if uat:
        uat_display = UAT_DISPLAY.get(uat, "UNKNOW UAT %d" % outcome)
        msg += " UAT: " % uat_display

    print(msg)


if __name__ == "__main__":
    raws_path, partials_path, all_titles_path = file_storage.check_and_config(imp="wiki")
    conn = Driver(imp="wiki", raws=raws_path)

    open_listings(conn, all_titles_path, DESIRED_PLATFORMS)
    titles = file_storage.unpack_all_titles(all_titles_path)
    for title in titles:
        out, did_redir, uat, hits = open_article(conn, title[0], title[1])
        open_article_to_tty(title[0], out, did_redir, uat, hits)
