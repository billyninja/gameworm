CREATE DATABASE gameworm_wikipedia
WITH OWNER = postgres
ENCODING = 'UTF8'
TABLESPACE = pg_default
LC_COLLATE = 'en_US.UTF-8'
LC_CTYPE = 'en_US.UTF-8'
CONNECTION LIMIT = -1;

\c gameworm_wikipedia;

CREATE TABLE public.article_info
(
    pk integer NOT NULL,
    source_title character varying(256) NOT NULL,
    final_title character varying(256) NOT NULL,
    wiki_page_id integer NOT NULL,
    main_infobox_subject character varying(32) NOT NULL,
    source_platform_slug character varying(32) NOT NULL,
    franchise_article boolean NOT NULL,
    unassertive_article_type smallint,
    UAT_section_pointer smallint,
    CONSTRAINT article_info_pkey PRIMARY KEY (pk)
);


CREATE TABLE public.assertive_game_info
(
    wiki_page_id integer NOT NULL,
    reliable boolean NOT NULL,
    wikimedia_image character varying(256) NOT NULL,
    image_caption character varying(256) NOT NULL,
    plaforms    character varying(32)[],
    genres    character varying(32)[],
    game_modes    character varying(32)[]
);

CREATE TABLE public.game_info_engine(
    pk integer NOT NULL,
    game_wpi integer NOT NULL,
    name character varying(128) NOT NULL,
    obs character varying(256)
);

CREATE TABLE public.game_info_author(
    pk integer NOT NULL,
    game_wpi integer NOT NULL,
    author_role smallint NOT NULL,   -- designer/programmer/director/producer/composer/writer
    name character varying(128) NOT NULL,
    obs character varying(256)
);

CREATE TABLE public.game_info_company(
    pk integer NOT NULL,
    game_wpi integer NOT NULL,
    company_role smallint NOT NULL,   -- designer/programmer/director/producer/composer/writer
    company_name character varying(64) NOT NULL,
    obs character varying(256)
);

CREATE TABLE public.game_info_release(
    pk integer NOT NULL,
    game_wpi integer NOT NULL,
    region_code character varying(4),
    plaform_slug character varying(32),
    release_date date,
    obs character varying(256)
);
