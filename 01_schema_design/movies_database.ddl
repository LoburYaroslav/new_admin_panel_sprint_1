CREATE SCHEMA IF NOT EXISTS content;

SET search_path = "content";

CREATE TABLE IF NOT EXISTS film_work
(
    id            uuid PRIMARY KEY,
    title         TEXT NOT NULL,
    description   TEXT,
    creation_date DATE,
    rating        FLOAT,
    type          TEXT NOT NULL,
    created       timestamp with time zone,
    modified      timestamp with time zone
);

CREATE TABLE IF NOT EXISTS person
(
    id        uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created   timestamp with time zone,
    modified  timestamp with time zone
);

-- Тк никаких вводных на счет хранения удаленных данных не было, думаю, что целостностью БД должна все-таки заниматься БД.
-- Поэтому везде пишу REFERENCES, из личных соображений с RESTRICT.
CREATE TABLE IF NOT EXISTS person_film_work
(
    id           uuid PRIMARY KEY,
    film_work_id uuid NOT NULL REFERENCES film_work (id) ON DELETE RESTRICT,
    person_id    uuid NOT NULL REFERENCES person (id) ON DELETE RESTRICT,
    role         TEXT NOT NULL,
    created      timestamp with time zone
);

-- Уникальный индекс создал по трем колонкам тк в одном фильме один человек вполне может играть РАЗНЫЕ роли, а вот одну и туже роль нет.
CREATE UNIQUE INDEX IF NOT EXISTS film_work_person_idx ON person_film_work (film_work_id, person_id, role);

CREATE TABLE IF NOT EXISTS genre
(
    id          uuid PRIMARY KEY,
    name        TEXT NOT NULL,
    description TEXT,
    created     timestamp with time zone,
    modified    timestamp with time zone
);

CREATE TABLE IF NOT EXISTS genre_film_work
(
    id           uuid PRIMARY KEY,
    genre_id     uuid NOT NULL REFERENCES genre (id) ON DELETE RESTRICT,
    film_work_id uuid NOT NULL REFERENCES film_work (id) ON DELETE RESTRICT,
    created      timestamp with time zone
);

CREATE UNIQUE INDEX IF NOT EXISTS film_work_genre_idx ON genre_film_work (film_work_id, genre_id);