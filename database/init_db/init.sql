CREATE TABLE users (
    user_id numeric NOT NULL UNIQUE,
    lang varchar(2) NOT NULL,
    purchases numeric,
    start_date timestamp NOT NULL
);

CREATE TABLE admins (
    username varchar NOT NULL UNIQUE,
    position varchar
);