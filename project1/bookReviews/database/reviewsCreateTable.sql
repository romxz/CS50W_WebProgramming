CREATE TABLE reviews (
    uid INTEGER REFERENCES users,
    isbn VARCHAR REFERENCES books,
    rating FLOAT(2) NOT NULL,
    review VARCHAR NOT NULL,
    PRIMARY KEY (uid, isbn)
);