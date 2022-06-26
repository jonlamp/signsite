DROP TABLE IF EXISTS signs CASCADE;
DROP TABLE IF EXISTS personalities CASCADE;
DROP TABLE IF EXISTS responses CASCADE;

CREATE TABLE signs (
    id SERIAL PRIMARY KEY ,
    star_sign TEXT UNIQUE NOT NULL,
    sign_description TEXT NOT NULL
);

CREATE TABLE personalities (
    id SERIAL PRIMARY KEY,
    personality TEXT UNIQUE NOT NULL,
    personality_description TEXT NOT NULL
);

CREATE TABLE responses (
    id SERIAL PRIMARY KEY,
    sign_id INTEGER NOT NULL,
    personality_id INTEGER NOT NULL,
    selection INTEGER NOT NULL, 
    submitted TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY(sign_id) REFERENCES signs(id),
    FOREIGN KEY(personality_id) REFERENCES personalities(id)
);