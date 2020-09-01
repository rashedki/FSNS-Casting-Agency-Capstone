--
-- PostgreSQL database dump
--

-- Dumped from database version 12.4
-- Dumped by pg_dump version 12.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: actors; Type: TABLE; Schema: public; Owner: khalil
--

CREATE TABLE public.actors (
    id integer NOT NULL,
    name character varying,
    age integer,
    gender character varying,
    movie_id integer
);


ALTER TABLE public.actors OWNER TO khalil;

--
-- Name: actors_id_seq; Type: SEQUENCE; Schema: public; Owner: khalil
--

CREATE SEQUENCE public.actors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.actors_id_seq OWNER TO khalil;

--
-- Name: actors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: khalil
--

ALTER SEQUENCE public.actors_id_seq OWNED BY public.actors.id;


--
-- Name: movies; Type: TABLE; Schema: public; Owner: khalil
--

CREATE TABLE public.movies (
    id integer NOT NULL,
    title character varying,
    release_date date
);


ALTER TABLE public.movies OWNER TO khalil;

--
-- Name: movies_id_seq; Type: SEQUENCE; Schema: public; Owner: khalil
--

CREATE SEQUENCE public.movies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.movies_id_seq OWNER TO khalil;

--
-- Name: movies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: khalil
--

ALTER SEQUENCE public.movies_id_seq OWNED BY public.movies.id;


--
-- Name: actors id; Type: DEFAULT; Schema: public; Owner: khalil
--

ALTER TABLE ONLY public.actors ALTER COLUMN id SET DEFAULT nextval('public.actors_id_seq'::regclass);


--
-- Name: movies id; Type: DEFAULT; Schema: public; Owner: khalil
--

ALTER TABLE ONLY public.movies ALTER COLUMN id SET DEFAULT nextval('public.movies_id_seq'::regclass);


--
-- Data for Name: actors; Type: TABLE DATA; Schema: public; Owner: khalil
--

COPY public.actors (id, name, age, gender, movie_id) FROM stdin;
1	khalil	10	M	1
2	actor2	20	F	2
3	actor3	30	M	3
4	actor4	40	F	4
\.


--
-- Data for Name: movies; Type: TABLE DATA; Schema: public; Owner: khalil
--

COPY public.movies (id, title, release_date) FROM stdin;
1	test movie title 1	2020-01-01
2	test movie title 2	2020-01-02
3	test movie title 3	2020-01-03
4	test movie title 4	2020-01-04
\.


--
-- Name: actors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: khalil
--

SELECT pg_catalog.setval('public.actors_id_seq', 4, true);


--
-- Name: movies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: khalil
--

SELECT pg_catalog.setval('public.movies_id_seq', 4, true);


--
-- Name: actors actors_pkey; Type: CONSTRAINT; Schema: public; Owner: khalil
--

ALTER TABLE ONLY public.actors
    ADD CONSTRAINT actors_pkey PRIMARY KEY (id);


--
-- Name: movies movies_pkey; Type: CONSTRAINT; Schema: public; Owner: khalil
--

ALTER TABLE ONLY public.movies
    ADD CONSTRAINT movies_pkey PRIMARY KEY (id);


--
-- Name: actors actors_movie_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: khalil
--

ALTER TABLE ONLY public.actors
    ADD CONSTRAINT actors_movie_id_fkey FOREIGN KEY (movie_id) REFERENCES public.movies(id);


--
-- PostgreSQL database dump complete
--

