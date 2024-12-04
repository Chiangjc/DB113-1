-- Table: public.factory

-- DROP TABLE IF EXISTS public.factory;

CREATE TABLE IF NOT EXISTS public.factory
(
    f_id bigint NOT NULL,
    f_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    f_country character varying(20) COLLATE pg_catalog."default" NOT NULL,
    f_address character varying(100) COLLATE pg_catalog."default" NOT NULL,
    f_phone character varying(20) COLLATE pg_catalog."default" NOT NULL,
    super_id bigint NOT NULL,
    CONSTRAINT factory_backup_pkey PRIMARY KEY (f_id),
    CONSTRAINT factory_backup_super_id_fkey FOREIGN KEY (super_id)
        REFERENCES public.employee (e_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_super_id FOREIGN KEY (super_id)
        REFERENCES public.employee (e_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.factory
    OWNER to postgres;