-- Table: public.rate

-- DROP TABLE IF EXISTS public.rate;

CREATE TABLE IF NOT EXISTS public.rate
(
    score integer NOT NULL,
    year integer NOT NULL,
    s_id bigint NOT NULL,
    e_id bigint NOT NULL,
    CONSTRAINT rate_backup_pkey PRIMARY KEY (score, year, s_id, e_id),
    CONSTRAINT fk_e_id FOREIGN KEY (e_id)
        REFERENCES public.employee (e_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_s_id FOREIGN KEY (s_id)
        REFERENCES public.supplier (s_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT rate_backup_e_id_fkey FOREIGN KEY (e_id)
        REFERENCES public.employee (e_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT rate_backup_s_id_fkey FOREIGN KEY (s_id)
        REFERENCES public.supplier (s_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.rate
    OWNER to postgres;