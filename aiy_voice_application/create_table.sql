CREATE TABLE action_button (
	action_id	SERIAL	PRIMARY KEY,
	action_time	timestamp with time zone	NOT NULL,
	question	text,
	answer	text,
	success_read	boolean	NOT NULL,
	success_answer	boolean NOT NULL
);

CREATE TABLE detect_human (
	detect_id	SERIAL	PRIMARY KEY,
	detect_time	timestamp with time zone	NOT NULL,
	is_detected	boolean	NOT NULL,
	error	boolean NOT NULL
);

CREATE TABLE list_music (
	music_id	SERIAL	PRIMARY KEY,
	file_name	varchar(64)	NOT NULL,
	extension	varchar(8) NOT NULL,
	file_path	varchar(128)	NOT NULL
);

CREATE TABLE auth_role (
	role_id	SERIAL	PRIMARY KEY,
	role_name	varchar(16)	NOT NULL,
	role_description	text
);

CREATE TABLE auth_user (
	user_id	SERIAL	PRIMARY KEY,
	user_fname	varchar(32)	NOT NULL,
	user_lname	varchar(32)	NOT NULL,
	pwd	varchar(128)	NOT NULL,
	active	boolean	NOT NULL,
	e_mail	varchar(128)	UNIQUE NOT NULL,
	user_description	text
);

CREATE TABLE auth_user_role (
	user_id	INTEGER	NOT NULL UNIQUE,
	role_id	INTEGER	NOT NULL,
	creation_time	timestamp with time zone	NOT NULL,
	expiration_time	timestamp with time zone	NOT NULL,
	FOREIGN KEY (user_id) REFERENCES auth_user(user_id),
	FOREIGN KEY (role_id) REFERENCES auth_role(role_id)
);

CREATE TABLE connection_status (
	connection_id	SERIAL	PRIMARY KEY,
	user_id	INTEGER	NOT NULL UNIQUE,
	user_ip	varchar(32)	NOT NULL UNIQUE,
	status	varchar(16)	NOT NULL,
	FOREIGN KEY (user_id) REFERENCES auth_user(user_id)
);

CREATE TABLE demand_app (
	demand_id	SERIAL	PRIMARY KEY,
	user_id	INTEGER	NOT NULL,
	demand_time	timestamp with time zone	NOT NULL,
	demand	text,
	response	text,
	FOREIGN KEY (user_id) REFERENCES auth_user(user_id)
);