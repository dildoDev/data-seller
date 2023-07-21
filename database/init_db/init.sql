CREATE TABLE users (
    user_id numeric NOT NULL UNIQUE,
    lang varchar(2) NOT NULL,
    purchases numeric,
    start_date timestamp NOT NULL
);

CREATE TABLE admins (
    user_id numeric NOT NULL UNIQUE,
    position varchar
);