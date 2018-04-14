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
    from tag_match import extract_sequence
    import json
    fh = open("samples.json", "r")
    ct = fh.read()
    releases = json.loads(ct)
    for rr in releases:
        sq = extract_sequence(rr)
        import pdb; pdb.set_trace()

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
