DROP DATABASE IF EXISTS gameworm_wikipedia;

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

CREATE SEQUENCE article_info_pk_seq;
ALTER TABLE article_info ALTER COLUMN pk SET DEFAULT nextval('article_info_pk_seq');
ALTER TABLE article_info ALTER COLUMN franchise_article SET DEFAULT FALSE;
ALTER TABLE article_info ALTER COLUMN pk SET NOT NULL;
ALTER SEQUENCE article_info_pk_seq OWNED BY article_info.pk;


CREATE TABLE public.assertive_game_info
(
    pk              integer NOT NULL,
    wiki_page_id    integer NOT NULL,
    reliable        boolean NOT NULL,
    wikimedia_image character varying(256),
    image_caption   character varying(256),
    game_modes      character varying(128)[],
    genres          character varying(128)[],
    CONSTRAINT assertive_game_info_pkey PRIMARY KEY (pk)
);

CREATE SEQUENCE game_info_pk_seq;
ALTER TABLE assertive_game_info ALTER COLUMN pk SET DEFAULT nextval('game_info_pk_seq');
ALTER TABLE assertive_game_info ALTER COLUMN pk SET NOT NULL;
ALTER SEQUENCE game_info_pk_seq OWNED BY assertive_game_info.pk;


CREATE TABLE public.game_info_engine(
    pk integer NOT NULL,
    game_wpi integer NOT NULL,
    name character varying(128) NOT NULL,
    obs character varying(256),
    CONSTRAINT game_info_engine_pkey PRIMARY KEY (pk)
);

CREATE SEQUENCE game_engine_pk_seq;
ALTER TABLE game_info_engine ALTER COLUMN pk SET DEFAULT nextval('game_engine_pk_seq');
ALTER TABLE game_info_engine ALTER COLUMN pk SET NOT NULL;
ALTER SEQUENCE game_engine_pk_seq OWNED BY game_info_engine.pk;


CREATE TABLE public.game_info_genre(
    pk integer NOT NULL,
    game_wpi integer NOT NULL,
    genre character varying(128) NOT NULL,
    CONSTRAINT game_info_genre_pkey PRIMARY KEY (pk)
);

CREATE SEQUENCE game_genre_pk_seq;
ALTER TABLE game_info_genre ALTER COLUMN pk SET DEFAULT nextval('game_genre_pk_seq');
ALTER TABLE game_info_genre ALTER COLUMN pk SET NOT NULL;
ALTER SEQUENCE game_genre_pk_seq OWNED BY game_info_genre.pk;



CREATE TABLE public.game_info_platform(
    pk integer NOT NULL,
    game_wpi integer NOT NULL,
    platform_code character varying(16) NOT NULL,
    CONSTRAINT game_info_platform_pkey PRIMARY KEY (pk)
);

CREATE SEQUENCE game_platform_pk_seq;
ALTER TABLE game_info_platform ALTER COLUMN pk SET DEFAULT nextval('game_platform_pk_seq');
ALTER TABLE game_info_platform ALTER COLUMN pk SET NOT NULL;
ALTER SEQUENCE game_platform_pk_seq OWNED BY game_info_platform.pk;



CREATE TABLE public.game_info_author(
    pk integer NOT NULL,
    game_wpi integer NOT NULL,
    author_role character varying(32),   -- designer/programmer/director/producer/composer/writer
    name character varying(128) NOT NULL,
    obs character varying(256),
    CONSTRAINT game_info_author_pkey PRIMARY KEY (pk)
);

CREATE SEQUENCE game_author_pk_seq;
ALTER TABLE game_info_author ALTER COLUMN pk SET DEFAULT nextval('game_author_pk_seq');
ALTER TABLE game_info_author ALTER COLUMN pk SET NOT NULL;
ALTER SEQUENCE game_author_pk_seq OWNED BY game_info_author.pk;


CREATE TABLE public.game_info_company(
    pk integer NOT NULL,
    game_wpi integer NOT NULL,
    company_role character varying(32),   -- designer/programmer/director/producer/composer/writer
    company_name character varying(64) NOT NULL,
    obs character varying(256),
    CONSTRAINT game_info_company_pkey PRIMARY KEY (pk)
);

CREATE SEQUENCE game_company_pk_seq;
ALTER TABLE game_info_company ALTER COLUMN pk SET DEFAULT nextval('game_company_pk_seq');
ALTER TABLE game_info_company ALTER COLUMN pk SET NOT NULL;
ALTER SEQUENCE game_company_pk_seq OWNED BY game_info_company.pk;


CREATE TABLE public.game_info_release(
    pk integer NOT NULL,
    game_wpi integer NOT NULL,
    region_code character varying(16),
    platform_slug character varying(32),
    release_date date,
    obs character varying(256),
    CONSTRAINT game_info_release_pkey PRIMARY KEY (pk)
);


CREATE SEQUENCE game_release_pk_seq;
ALTER TABLE game_info_release ALTER COLUMN pk SET DEFAULT nextval('game_release_pk_seq');
ALTER TABLE game_info_release ALTER COLUMN pk SET NOT NULL;
ALTER SEQUENCE game_release_pk_seq OWNED BY game_info_release.pk;
