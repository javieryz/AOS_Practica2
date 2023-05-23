FROM mysql:latest

COPY aos.sql /docker-entrypoint-initdb.d/

ENV MYSQL_ROOT_PASSWORD=aos2023
ENV MYSQL_DATABASE=aos2023

EXPOSE 3306