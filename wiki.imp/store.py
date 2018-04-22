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


def insert_article_info(a, b, c, d):
    print("here")
    return


def insert_game_info(article_info, game_info_core, authors=[], companies=[], engines=[], releases=[]):
    print("here")
    return
