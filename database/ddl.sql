DROP TABLE IF EXISTS alura_flask.games_db;
CREATE TABLE alura_flask.games_db (
    id INTEGER NOT NULL AUTO_INCREMENT,
    name VARCHAR(64) NOT NULL,
    category VARCHAR(32) NOT NULL,
    console VARCHAR(16) NOT NULL,
    PRIMARY KEY(id)
-- ) CHARSET=utf-8 COLLATE=utf-8_bin;
);

DROP TABLE IF EXISTS alura_flask.users_db;
CREATE TABLE alura_flask.users_db (
    id INTEGER NOT NULL AUTO_INCREMENT,
    username VARCHAR(16) NOT NULL,
    name VARCHAR(256) NOT NULL,
    password VARCHAR(128) NOT NULL,
    PRIMARY KEY(id)
-- ) CHARSET=utf-8 COLLATE=utf-8_bin;
);
