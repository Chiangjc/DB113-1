-- Table: public.inventory_from_factory

-- DROP TABLE IF EXISTS public.inventory_from_factory;

CREATE TABLE IF NOT EXISTS public.inventory_from_factory
(
    inv_id bigint NOT NULL,
    f_id bigint NOT NULL,
    year integer NOT NULL,
    CONSTRAINT inventory_from_factory_backup_pkey PRIMARY KEY (inv_id, f_id, year),
    CONSTRAINT fk_f_id FOREIGN KEY (f_id)
        REFERENCES public.factory (f_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_inv_id FOREIGN KEY (inv_id)
        REFERENCES public.inventory (inv_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT inventory_from_factory_backup_f_id_fkey FOREIGN KEY (f_id)
        REFERENCES public.factory (f_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT inventory_from_factory_backup_inv_id_fkey FOREIGN KEY (inv_id)
        REFERENCES public.inventory (inv_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.inventory_from_factory
    OWNER to postgres;