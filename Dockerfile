FROM postgres:latest
ENV POSTGRES_USER=admin_user POSTGRES_PASSWORD=admin POSTGRES_DB=admin_db
COPY init.sql /docker-entrypoint-initdb.d/