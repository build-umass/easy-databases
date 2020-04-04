FROM postgres:latest
# The postgres Docker container in Docker Hub uses environment variables
# to set the username/password of the Postgres super user
# and the name of the default database.
ENV POSTGRES_USER=admin_user POSTGRES_PASSWORD=admin POSTGRES_DB=admin_db
COPY init.sql /docker-entrypoint-initdb.d/