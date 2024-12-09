-- Table: public.part

-- DROP TABLE IF EXISTS public.part;

CREATE TABLE IF NOT EXISTS public.part
(
    p_id bigint NOT NULL,
    p_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    standard character varying(100) COLLATE pg_catalog."default" NOT NULL,
    length double precision NOT NULL,
    width double precision NOT NULL,
    height double precision NOT NULL,
    CONSTRAINT part_backup_pkey PRIMARY KEY (p_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.part
    OWNER to postgres;