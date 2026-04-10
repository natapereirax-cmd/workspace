CREATE DATABASE IF NOT EXISTS workspace_db;
USE workspace_db;

-- USERS
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    
    username VARCHAR(50) NOT NULL,
    
    email VARCHAR(100) NOT NULL UNIQUE,
    
    password VARCHAR(255) NOT NULL,
    salt VARBINARY(16) NOT NULL,

    CHECK (firstname REGEXP '^[A-Za-z]+$'),
    CHECK (lastname REGEXP '^[A-Za-z]+$')
);


-- CATEGORIES
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(100) NOT NULL,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    user_id INT NOT NULL,

    FOREIGN KEY (user_id) 
    REFERENCES users(id)
    ON DELETE CASCADE
);


-- TASKS
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(150) NOT NULL,

    description TEXT,

    priority INT DEFAULT 1,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    due_date DATETIME,

    completed_at DATETIME,

    status VARCHAR(30) DEFAULT 'pending',

    user_id INT NOT NULL,

    category_id INT,

    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE,

    FOREIGN KEY (category_id)
    REFERENCES categories(id)
    ON DELETE SET NULL
);


-- ACTIVITY
CREATE TABLE activity (
    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    message TEXT NOT NULL,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE
);