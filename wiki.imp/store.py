"""Information containers organization."""


class ArticleInfo:

    def __init__(self, src_title, final_title, wpi, infobox_subject, src_platform_slug, unspecific_article_type,
                 uat_section_pointer):
        pass


class GameInfoCore:

    def __init__(self, wpi, reliable, wikimedia_image, image_caption, platforms, genres, game_modes):
        pass


class GameInfoAuthor:

    def __init__(self, wpi, name, role, obs=None):
        pass


class GameInfoCompany:

    def __init__(self, wpi, name, role, obs=None):
        pass


class GameInfoGenre:

    def __init__(self, wpi, name):
        pass


class GameInfoEngine:

    def __init__(self, wpi, name, obs=None):
        pass


class GameInfoRelease:

    def __init__(self, platform, region=None, rdate=None):
        self.platform = platform
        self.region = region
        self.rdate = rdate

    def __repr__(self):
        return "[%s, %s, %s]" % (self.platform.code, self.region.vl, self.rdate.strftime("%B %d, %Y"))


article_insert = """
INSERT INTO article_info(
    source_title, final_title, wiki_page_id, main_infobox_subject, source_platform_slug,
    franchise_article, fc_correct_section, cross_media_article, cm_correct_section
VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')
"""

game_info_insert = """
INSERT INTO assertive_game_info(
    wiki_page_id, reliable, wikimedia_image, image_caption, platforms, genres, game_modes
VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')
"""

author_insert = """
INSERT INTO game_info_author(game_wpi, author_role, name)
VALUES ('%s', '%s', '%s')
"""

company_insert = """
INSERT INTO game_info_company(game_wpi, company_role, company_name)
VALUES ('%s', '%s', '%s')
"""

engine_insert = """
INSERT INTO game_info_engine(game_wpi, name)
VALUES ('%s', '%s')
"""

release_insert = """
INSERT INTO game_info_engine(game_wpi, region_code, plaform_slug, release_date)
VALUES ('%s', '%s', '%s', '%s')
"""


def insert_game_info(article_info, game_info_core, authors=[], companies=[], engines=[], releases=[]):
    return
