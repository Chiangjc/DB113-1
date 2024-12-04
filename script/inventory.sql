-- Table: public.inventory

-- DROP TABLE IF EXISTS public.inventory;

CREATE TABLE IF NOT EXISTS public.inventory
(
    inv_id bigint NOT NULL,
    inv_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    status character varying(100) COLLATE pg_catalog."default" NOT NULL,
    p_id bigint NOT NULL,
    CONSTRAINT inventory_backup_pkey PRIMARY KEY (inv_id),
    CONSTRAINT fk_p_id FOREIGN KEY (p_id)
        REFERENCES public.part (p_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT inventory_backup_p_id_fkey FOREIGN KEY (p_id)
        REFERENCES public.part (p_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.inventory
    OWNER to postgres;