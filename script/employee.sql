-- Table: public.employee

-- DROP TABLE IF EXISTS public.employee;

CREATE TABLE IF NOT EXISTS public.employee
(
    e_id bigint NOT NULL,
    e_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    start_date date NOT NULL,
    password character varying(20) COLLATE pg_catalog."default" NOT NULL,
    mgr_id bigint NOT NULL,
    CONSTRAINT employee_backup_pkey PRIMARY KEY (e_id),
    CONSTRAINT employee_backup_mgr_id_fkey FOREIGN KEY (mgr_id)
        REFERENCES public.employee (e_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_mgr_id FOREIGN KEY (mgr_id)
        REFERENCES public.employee (e_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.employee
    OWNER to postgres;