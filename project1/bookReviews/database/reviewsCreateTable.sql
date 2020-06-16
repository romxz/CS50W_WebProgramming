CREATE TABLE reviews (
    rid SERIAL PRIMARY KEY,
    uid INTEGER REFERENCES users,
    review VARCHAR NOT NULL,
    isbn INTEGER REFERENCES books,
    rating FLOAT(2) NOT NULL
);