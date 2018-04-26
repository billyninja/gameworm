"""bootstrap, start and control the pipeline as a whole."""
import sys
sys.path.append('../')

from constants import UAT_DISPLAY
from constants import ArticleOutcome as Ao, ARTICLE_OUTCOME_DISPLAY as AO_DISPLAY
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

NON_GAME_TITLES = [
    "[[MobyGames]]", "[[Capcom]]", "[[Konami]]", "[[Gameloft]]", "[[Rovio Entertainment]]", "[[LucasArts]]",
    "[[Ubisoft]]", "[[Action-adventure game|Action-adventure]]",
    "[[Stealth video game|stealth]]", "[[Puzzle video game|Puzzle]]", "[[Supergiant Games]]",
    "[[Warner Bros. Interactive Entertainment]]", "[[Adventure game|Adventure]]", "[[Rockstar Vancouver]]",
    "[[Rockstar Games]]", "[[First-person shooter]]", "[[King (website)|King]]",
    "[[Tile-matching video game|Tile-matching]]", "[[Double Fine Productions]]", "[[Sega]]",
    "[[Puzzle video game|Puzzle]]", "[[Platform game|platformer]]", "[[Square Enix]]",
    "[[Role-playing video game|RPG]]", "[[Strategy video game|Strategy]]",
    "[[Massively multiplayer online game|MMO]]", "[[Incygames Ltd]]", "[[Sega]]",
    "[[Racing video game|Racing]]", "[[Arcade game|arcade]]", "[[Platform game|endless runner]]", "[[ZeptoLab]]",
    "[[Interactive fiction]]", "[[Bullet hell]]", "[[Platform game|Platformer]]", "[[Bethesda Softworks]]",
    "[[Collectible card game|Collectible card]]", "[[Survival horror]]", "[[T&E Soft]]", "[[Irem (company)|Irem]]",
    "[[Activision]]", "[[Ubisoft Montreal]]", "[[Sony Computer Entertainment]]", "[[TinyCo]]",
    "[[City building game|City building]]", "[[Kairosoft]]", "[[Simulation video game|Simulation]]", "[[Tag Games]]",
    "[[Shoot 'em up|Run and gun]]", "[[Multiplayer online battle arena|MOBA]]", "[[Word game]]",
    "[[Platform game|platform]]", "[[Racing video game|racing]]", "[[Endless runner]]",
    "[[Platform game|Vertical platformer]]", "[[Interactive movie]]", "[[Nintendo]]", "[[Sega|Sega Networks Inc.]]",
    "[[Puzzle game|Puzzle]]", "[[Nintendo]]", "[[Terry Cavanagh (developer)|Terry Cavanagh]]",
    "[[Twitch gameplay|Twitch]]", "[[64DD]]", "[[Xbox]]", "[[IGN.com]]", "[[Macworld]]", "[[mobygames]]",
    "[[PlayStation (console)|PlayStation]]", "[[IndieCade]]",
    "[[Category:Video game lists by platform|Sega Master System]]", "[[MMOSG]]", "[[PlayChoice-10]]",
    "[[Shoot-em-up]]", "[[Xbox Live#Gamerscore|Gamerscore]]", "[[Virgin Interactive|Virgin Games]]",
    "[[SCE Studio San Diego]]", "[[i-mode]]", "[[Amiga Format]]", "[[sport video game]]", "[[Arcade game]]",
    "[[Nintendo VS. System]]", "[[Open world|Sandbox]]", "[[3D computer graphics|3D]]", "[[DirectX 9]]", "[[IBM-PC]]",
    "[[Xbox One]]"
]


EXPR = "(File\:|[0-9]{4}\sin|\(game(s)? publisher\)|\(publisher\)|\(game(s)? designer\)|\(composer\)|\(game(s)? programmer\)|\(game(s)? developer\)|\(video game(s)? designer\)|\(video game(s)? programmer\)|\(video game(s)? composer\)|\(software publisher\)|company\)|studios|Soft(ware)?|Co\.|Ltd\.|\[\[List(s)?\s|Entertainment)"


def explode_lists(conn, run_partials_path):
    import re
    import os
    from constants import NEW_LISTS
    from extract_info import outer_peel

    all_leads = []
    for al in NEW_LISTS:
        resp = conn.fetch(al)
        wpi, raw = outer_peel(resp)
        hot_leads = set(re.findall("\[\[[^<]+?\]\]", raw))
        for hl in hot_leads:
            if re.search(EXPR, hl, flags=re.I) or hl in NON_GAME_TITLES:
                continue
            all_leads.append(hl)

        print(al, len(hot_leads))

    all_leads = list(set(all_leads))
    print(len(all_leads))
    fh = open(os.path.join(run_partials_path, "leads.txt"), 'w')
    fh.write("\n".join(all_leads))
    fh.flush()
    fh.close()

    return all_leads


def _reg_stats(stats, out):
    if out not in stats:
        stats.update({out: 1})
    else:
        stats[out] += 1


def _out_stats(stats):
    total = sum(stats.values())
    ostr = "\n %d" % total
    for k, v in stats.items():
        ostr += "| %s: %d (%.2f)" % (k, v, (v / total) * 100)
    print(ostr + "\n")


if __name__ == "__main__":
    from extract_info import macro
    import sys
    dir(sys)

    work_offline = "--offline" in sys.argv[1:]

    raws_path, run_partials_path = file_storage.check_and_config(imp="wiki")
    conn = Driver(imp="wiki", raws=raws_path, work_offline=work_offline)

    xx = macro(conn, "Philips Videopac + G7400")

    all_leads = explode_lists(conn, run_partials_path)
    stats = {}

    for lead in all_leads:
        out = macro(conn, lead)
        _reg_stats(stats, out)
        _out_stats(stats)
