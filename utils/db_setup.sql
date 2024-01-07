
create table if not exists users (
    user_id serial PRIMARY KEY,
	username VARCHAR ( 500 ) UNIQUE NOT NULL,
	hashed_password bytea NOT NULL,
	email VARCHAR ( 500 ) UNIQUE NOT NULL,
	created_at TIMESTAMP NOT NULL
);