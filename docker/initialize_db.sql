CREATE DATABASE mds;
CREATE USER 'mds'@'localhost' IDENTIFIED BY 'mds';
GRANT ALL ON mds.* TO 'mds'@'localhost';