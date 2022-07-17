-- Accounts (or Users)
CREATE TABLE IF NOT EXISTS Accounts (
    id INTEGER PRIMARY KEY,
    account_email Varchar(50) NOT NULL,
    account_password TEXT NOT NULL,
    first_name Varchar(50) NOT NULL,
    last_name Varchar(50) NOT NULL,
    account_status Varchar(250),
    access_token TEXT NOT NULL,
    phone_number Varchar(24),
    account_level TEXT DEFAULT 'user',
    user_id Varchar(10) NOT NULL,
    gender INTEGER NOT NULL,
    birthday TEXT,
    create_date INTEGER NOT NULL
);

-- Notes
CREATE TABLE IF NOT EXISTS Notes (
    id INTEGER PRIMARY KEY,
    content TEXT NOT NULL,
    creator INTEGER NOT NULL,
    date INTEGER NOT NULL,
    note_id Varchar(10) NOT NULL,
    is_edited INT DEFAULT 0,
    FOREIGN KEY(creator) REFERENCES Accounts(id)
);

-- Friends
CREATE TABLE IF NOT EXISTS Friends (
    id INTEGER PRIMARY KEY,
    first_friend INTEGER NOT NULL,
    second_friend INTEGER NOT NULL,
    status Varchar(16) NOT NULL DEFAULT 'incoming',
    FOREIGN KEY(first_friend) REFERENCES Accounts(id),
    FOREIGN KEY(second_friend) REFERENCES Accounts(id)
);

-- Groups
CREATE TABLE IF NOT EXISTS Groups (
    id INTEGER PRIMARY KEY,
    create_time INTEGER NOT NULL,
    group_id TEXT NOT NULL,
    group_name Varchar(100) NOT NULL,
    group_status Varchar(250) NOT NULL, 
);

-- Subscribers (for groups)
CREATE TABLE IF NOT EXISTS Subscribers (
    id INTEGER PRIMARY KEY,
    subscriber INTEGER NOT NULL,
    subscribed_at INTEGER NOT NULL,
    subscriber_rank INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY(subscriber) REFERENCES Accounts(id),
    FOREIGN KEY(subscribed_at) REFERENCES Groups(id)
);

-- Posts
CREATE TABLE IF NOT EXISTS Posts (
    id INTEGER PRIMARY KEY,
    create_date INTEGER NOT NULL,
    post_id TEXT NOT NULL,
    content TEXT NOT NULL,
    group_creator INTEGER,
    user_creator INTEGER,
    FOREIGN KEY(user) REFERENCES Accounts(id),
    FOREIGN KEY(group_creator) REFERENCES Groups(id)
);

-- Likes
CREATE TABLE IF NOT EXISTS Likes (
    id INTEGER PRIMARY KEY,
    liked_post INTEGER NOT NULL,
    liked_user INTEGER NOT NULL,
    like_date INTEGER NOT NULL,
    FOREIGN KEY(liked_user) REFERENCES Accounts(id),
    FOREIGN KEY(liked_post) REFERENCES Posts(post_id)
)