-- Table: public.inventory_from_supplier

-- DROP TABLE IF EXISTS public.inventory_from_supplier;

CREATE TABLE IF NOT EXISTS public.inventory_from_supplier
(
    inv_id bigint NOT NULL,
    s_id bigint NOT NULL,
    year integer NOT NULL,
    CONSTRAINT inventory_from_supplier_backup_pkey PRIMARY KEY (inv_id, s_id, year),
    CONSTRAINT fk_inv_id FOREIGN KEY (inv_id)
        REFERENCES public.inventory (inv_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_s_id FOREIGN KEY (s_id)
        REFERENCES public.supplier (s_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT inventory_from_supplier_backup_inv_id_fkey FOREIGN KEY (inv_id)
        REFERENCES public.inventory (inv_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT inventory_from_supplier_backup_s_id_fkey FOREIGN KEY (s_id)
        REFERENCES public.supplier (s_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.inventory_from_supplier
    OWNER to postgres;