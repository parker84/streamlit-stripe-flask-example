

create table if not exists users (
    id serial PRIMARY KEY,
	username VARCHAR ( 500 ) UNIQUE NOT NULL,
	hashed_password bytea NOT NULL,
	email VARCHAR ( 500 ) UNIQUE NOT NULL,
	created_at TIMESTAMP NOT NULL,
	updated_at TIMESTAMP NOT NULL,
	status INT NOT NULL, -- 0: inactive, 1: active, 2: deleted
	stripe_customer_id VARCHAR ( 500 ) UNIQUE NOT NULL
);