INSERT INTO users (username, password)
VALUES
    ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
    ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');

INSERT INTO channels (topic, created)
VALUES
    ('test topic 1', '2020-07-26 00:00:00'),
    ('test topic 2', '2020-07-25 00:00:00');

INSERT INTO messages (channel_id, author_id, created, body)
VALUES
    (1, 1, '2020-07-26 00:00:00', 'test 1' || x'0a' || 'body 1'),
    (1, 2, '2020-07-27 00:00:00', 'test 1' || x'0a' || 'body 2'),
    (1, 1, '2020-07-28 00:00:00', 'test 1' || x'0a' || 'body 3');
