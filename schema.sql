DROP TABLE IF EXISTS urls;
DROP TABLE IF EXISTS AuthenticatedUsers;


CREATE TABLE urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    original_url TEXT NOT NULL,
    short_url_id TEXT NOT NULL,
    count INTEGER NOT NULL DEFAULT 0
);


CREATE TABLE AuthenticatedUsers (
    userId INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEST NOT NULL,
    password TEXT NOT NULL
);

INSERT INTO AuthenticatedUsers (username, password) VALUES
('user', 'userPassword');

INSERT INTO AuthenticatedUsers (username, password) VALUES
('admin', 'adminPassword');