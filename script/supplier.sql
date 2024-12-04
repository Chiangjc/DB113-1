-- Table: public.supplier

-- DROP TABLE IF EXISTS public.supplier;

CREATE TABLE IF NOT EXISTS public.supplier
(
    s_id bigint NOT NULL,
    s_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    s_country character varying(20) COLLATE pg_catalog."default" NOT NULL,
    s_address character varying(100) COLLATE pg_catalog."default" NOT NULL,
    s_phone character varying(20) COLLATE pg_catalog."default" NOT NULL,
    super_name character varying(20) COLLATE pg_catalog."default",
    CONSTRAINT supplier_backup_pkey PRIMARY KEY (s_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.supplier
    OWNER to postgres;