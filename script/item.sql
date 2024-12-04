-- Table: public.item

-- DROP TABLE IF EXISTS public.item;

CREATE TABLE IF NOT EXISTS public.item
(
    parent_inv bigint NOT NULL,
    child_inv bigint NOT NULL,
    CONSTRAINT item_backup_pkey PRIMARY KEY (parent_inv, child_inv),
    CONSTRAINT fk_child_inv FOREIGN KEY (child_inv)
        REFERENCES public.inventory (inv_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_parent_inv FOREIGN KEY (parent_inv)
        REFERENCES public.inventory (inv_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT item_backup_child_inv_fkey FOREIGN KEY (child_inv)
        REFERENCES public.inventory (inv_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT item_backup_parent_inv_fkey FOREIGN KEY (parent_inv)
        REFERENCES public.inventory (inv_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.item
    OWNER to postgres;