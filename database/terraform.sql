DROP DATABASE IF EXISTS alura_flask;
CREATE DATABASE alura_flask;
GRANT ALL PRIVILEGES ON alura_flask.* TO 'alura_mysql'@'%';
FLUSH PRIVILEGES;
