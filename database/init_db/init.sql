CREATE TABLE users (
    user_id numeric NOT NULL IF NOT EXISTS,
    lang varchar(2) NOT NULL,
    purchases numeric,
    start_date timestamp NOT NULL
);

CREATE TABLE admins (
    user_id numeric NOT NULL IF NOT EXISTS,
    position varchar
);