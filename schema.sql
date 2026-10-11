-- Research Opportunity Portal: database setup
-- Run with:  sudo mysql < schema.sql
-- IMPORTANT: change 'change_me' below to your own password,
-- and use the same password in your .env file.

CREATE DATABASE IF NOT EXISTS research_portal;

CREATE USER IF NOT EXISTS 'flaskuser'@'localhost' IDENTIFIED BY 'change_me';
GRANT ALL PRIVILEGES ON research_portal.* TO 'flaskuser'@'localhost';
FLUSH PRIVILEGES;

USE research_portal;

-- Same structure Flask-SQLAlchemy creates from the Opportunity model
CREATE TABLE IF NOT EXISTS opportunity (
    id           INT          NOT NULL AUTO_INCREMENT,
    title        VARCHAR(200) NOT NULL,
    description  TEXT         NOT NULL,
    area         VARCHAR(100) NOT NULL,
    faculty_name VARCHAR(100) NOT NULL,
    department   VARCHAR(100) NOT NULL,
    skills       VARCHAR(255),
    positions    INT          NOT NULL,
    deadline     VARCHAR(20)  NOT NULL,
    status       VARCHAR(10)  DEFAULT 'Open',
    PRIMARY KEY (id)
);
