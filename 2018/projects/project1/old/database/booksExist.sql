SELECT EXISTS (
    SELECT FROM information_schema.tables
    WHERE table_schema = 'public' AND table_name = 'books'
);