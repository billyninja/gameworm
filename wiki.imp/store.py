class ArticleInfo:

    def __init__(self, src_title, final_title, wpi, infobox_subject, src_platform_slug, unspecific_article_type,
                 uat_section_pointer):
        pass


class GameInfoCore:

    def __init__(self, wpi, reliable, wikimedia_image, image_caption, plaforms, genres, game_modes):
        pass


class GameInfoAuthor:

    def __init__(self, wpi, name, role, obs):
        pass


class GameInfoCompany:

    def __init__(self, wpi, name, role, obs):
        pass


class GameInfoEngine:

    def __init__(self, wpi, name, obs):
        pass


class GameInfoRelease:

    def __init__(self, wpi, region_code, plaform_slug, release_date, obs):
        pass


def insert_into_db(article_info, game_info_core, authors=[], companies=[], engines=[], releases=[]):
    return
