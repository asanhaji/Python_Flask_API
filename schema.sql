CREATE TABLE IF NOT EXISTS users(
    id INTEGER primary key autoincrement,
    username TEXT not null,
    email TEXT not null,
    password TEXT not null
);

