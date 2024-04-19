-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS BlogBite;
CREATE USER IF NOT EXISTS 'raziel'@'localhost' IDENTIFIED BY 'blogbitepass';
GRANT ALL PRIVILEGES ON `BlogBite`.* TO 'raziel'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'raziel'@'localhost';
FLUSH PRIVILEGES;