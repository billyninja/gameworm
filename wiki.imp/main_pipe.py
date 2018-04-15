"""bootstrap, start and control the pipeline as a whole."""
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
        Ao.NO_INFOBOX_ARTICLE: colors.neutral_bland,
    }

    ao_display = AO_DISPLAY.get(outcome, "UNKNOW ARTICLE OUTCOME %d" % outcome)
    msg = ao_tty_colors[outcome](title + " - " + ao_display, bold=True)

    if did_redir:
        msg += " -> Redir"

    if uat:
        uat_display = UAT_DISPLAY.get(uat, "UNKNOW UAT %d" % outcome)
        msg += " UAT: " % uat_display

    print(msg)


if __name__ == "__main__":
    # TMP
    from tag_match import extract_sequence, identify_sequence, sequence_p_r_d
    import json
    from time import sleep

    # inp = 'Released:§*March 3, 1995 (Win)§*1996 (Mac)§*November 15, 2011, August 13, 2015 (iOS)§*2012 (Android)§*2014 (Linux)§*July 3, 2014 (Steam)§Re-released:§*January 12, 1999§*October 2005'

    # sq = extract_sequence(inp)
    # print(sq)
    # import pdb; pdb.set_trace()
    # raise ValueError(1)

    # fh = open("samples.json", "r")
    # ct = fh.read()
    # cnt = 0
    # releases = json.loads(ct)
    # for rr in releases:
    #     sq = extract_sequence(rr)
    #     stype = identify_sequence(sq)
    #     if stype == "P-R-D":
    #         xx = sequence_p_r_d(sq)
    #         print("PRD", len(xx))
    #         cnt += 1
    #         continue

    #     if stype == "R-D-P":
    #         print("R-D-P")
    #         cnt += 1
    #     elif stype == "simple date":
    #         cnt += 1
    #         print("simple")
    #     elif stype == "R-D":
    #         cnt += 1
    #         print("RD")
    #     elif stype == "D-P":
    #         cnt += 1
    #         print("DP")
    #     else:
    #         import pdb; pdb.set_trace()
    #         print("x: miss", stype)

    # print(cnt)
    # raise ValueError(1)
    raws_path, run_partials_path = file_storage.check_and_config(imp="wiki")
    conn = Driver(imp="wiki", raws=raws_path)

    all_titles, all_titles_path = open_listings(conn, run_partials_path, DESIRED_PLATFORMS)

    stats = {}

    def _reg_stats(out):
        if out not in stats:
            stats.update({out: 1})
        else:
            stats[out] += 1

    for title in all_titles:
        out, did_redir, uat, hits = open_article(conn, title[0], title[1])
        _reg_stats(out)
        open_article_to_tty(title[0], out, did_redir, uat, hits)

    from article_pipe import samples
    import json

    ff = open("samples.json", "w")
    ff.write(json.dumps(samples))
    ff.flush()
    ff.close()

    print(stats)
