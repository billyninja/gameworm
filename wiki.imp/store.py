"""Information containers organization."""
import psycopg2


conn = psycopg2.connect("dbname=gameworm_wikipedia user=postgres password=postgres")


class ArticleInfo:

    def __init__(self, src_title, final_title, wpi, infobox_subject, src_platform_slug, unspecific_article_type,
                 uat_section_pointer):
        self.src_title = src_title
        self.final_title = final_title
        self.wpi = wpi
        self.infobox_subject = infobox_subject
        self.src_platform_slug = src_platform_slug
        self.unspecific_article_type = unspecific_article_type,
        self.uat_section_pointer = uat_section_pointer


class GameInfoCore:

    def __init__(self, wpi, reliable, wikimedia_image, image_caption, genres, game_modes):
        self.wpi = wpi
        self.reliable = reliable
        self.wikimedia_image = wikimedia_image
        self.image_caption = image_caption
        self.genres = genres
        self.game_modes = game_modes


class GameInfoAuthor:

    def __init__(self, wpi, name, role, obs=None):
        self.wpi = wpi
        self.name = name
        self.role = role


class GameInfoCompany:

    def __init__(self, wpi, name, role, obs=None):
        self.wpi = wpi
        self.name = name
        self.role = role


class GameInfoGenre:

    def __init__(self, wpi, name):
        self.wpi = wpi
        self.name = name


class GameInfoEngine:

    def __init__(self, wpi, name, obs=None):
        self.wpi = wpi
        self.name = name


class GameInfoRelease:

    def __init__(self, platform, region=None, rdate=None):
        self.platform = platform
        self.region = region
        self.rdate = rdate

    def __repr__(self):
        return "[%s, %s, %s]" % (self.platform.code, self.region.vl, self.rdate.strftime("%B %d, %Y"))


ARTICLE_INSERT = """
INSERT INTO article_info(
    source_title,
    final_title,
    wiki_page_id,
    main_infobox_subject,
    source_platform_slug,
    franchise_article,
    unassertive_article_type,
    UAT_section_pointer
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
"""

GAME_INFO_INSERT = """
INSERT INTO assertive_game_info(
    wiki_page_id,
    reliable,
    wikimedia_image,
    image_caption,
    genres,
    game_modes
) VALUES (%s, %s, %s, %s, %s, %s);
"""

AUTHOR_INSERT = """
INSERT INTO game_info_author(game_wpi, author_role, name)
VALUES (%s, %s, %s);
"""

COMPANY_INSERT = """
INSERT INTO game_info_company(game_wpi, company_role, company_name)
VALUES (%s, %s, %s);
"""

ENGINE_INSERT = """
INSERT INTO game_info_engine(game_wpi, name)
VALUES (%s, %s);
"""


PLATFORM_INSERT = """
INSERT INTO game_info_platform(game_wpi, platform_code)
VALUES (%s, %s);
"""

RELEASE_INSERT = """
INSERT INTO game_info_release(game_wpi, region_code, platform_slug, release_date)
VALUES (%s, %s, %s, %s);
"""


def insert_game_info(article_info, game_info_core, platforms=[], authors=[], companies=[], engines=[], releases=[]):
    cur = conn.cursor()

    # TODO - bulk! atomic!
    ga = article_info
    params1 = [ga.src_title, ga.final_title, ga.wpi, ga.infobox_subject, ga.src_platform_slug, False,
               None, ga.uat_section_pointer]
    cur.execute(ARTICLE_INSERT, params1)

    gi = game_info_core
    params2 = [gi.wpi, gi.reliable, gi.wikimedia_image, gi.image_caption,
               [x.name for x in gi.genres], gi.game_modes]
    cur.execute(GAME_INFO_INSERT, params2)

    for plat in platforms:
        params3 = [ga.wpi, plat.code]
        cur.execute(PLATFORM_INSERT, params3)

    for auth in authors:
        params3 = [auth.wpi, auth.role, auth.name]
        cur.execute(AUTHOR_INSERT, params3)

    for comp in companies:
        params3 = [comp.wpi, comp.role, comp.name]
        cur.execute(COMPANY_INSERT, params3)

    for eng in engines:
        params3 = [eng.wpi, eng.name]
        cur.execute(ENGINE_INSERT, params3)

    for rel in releases:
        reg = "U/N"
        plat = "U/N"
        if rel.region:
            reg = rel.region.vl

        if rel.platform:
            plat = rel.platform.code

        params3 = [ga.wpi, reg, plat, rel.rdate]
        cur.execute(RELEASE_INSERT, params3)

    cur.close()
    conn.commit()
    return
