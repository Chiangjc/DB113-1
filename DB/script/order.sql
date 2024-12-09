-- Table: public.Order

-- DROP TABLE IF EXISTS public."Order";

CREATE TABLE IF NOT EXISTS public."Order"
(
    o_id bigint NOT NULL,
    order_date date NOT NULL,
    due_date date NOT NULL,
    arrive_date date,
    quantity integer NOT NULL,
    status character varying(100) COLLATE pg_catalog."default" NOT NULL DEFAULT 'Not Yet Shipped'::character varying,
    feedback character varying(100) COLLATE pg_catalog."default",
    e_id bigint NOT NULL,
    inv_id bigint NOT NULL,
    CONSTRAINT order_backup_pkey PRIMARY KEY (o_id),
    CONSTRAINT fk_e_id FOREIGN KEY (e_id)
        REFERENCES public.employee (e_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_inv_id FOREIGN KEY (inv_id)
        REFERENCES public.inventory (inv_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT order_backup_e_id_fkey FOREIGN KEY (e_id)
        REFERENCES public.employee (e_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT order_backup_inv_id_fkey FOREIGN KEY (inv_id)
        REFERENCES public.inventory (inv_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Order"
    OWNER to postgres;