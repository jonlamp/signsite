DROP TABLE IF EXISTS signs;
DROP TABLE IF EXISTS personalities;
DROP TABLE IF EXISTS responses;

CREATE TABLE signs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    star_sign TEXT UNIQUE NOT NULL,
    sign_description TEXT NOT NULL
);

CREATE TABLE personalities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    personality TEXT UNIQUE NOT NULL,
    personality_description TEXT NOT NULL
);

CREATE TABLE responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sign_id INTEGER NOT NULL,
    personality_id INTEGER NOT NULL,
    selection INTEGER NOT NULL, 
    submitted TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY(sign_id) REFERENCES signs(id),
    FOREIGN KEY(personality_id) REFERENCES personalities(id)
);