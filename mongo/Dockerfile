FROM mongo:latest
# The mongo Docker container in Docker Hub uses environment variables
# to set the username/password of the Mongo super user
# and the name of the default database.
ENV MONGO_INITDB_ROOT_USERNAME=admin_user MONGO_INITDB_ROOT_PASSWORD=admin MONGO_INITDB_DATABASE=admin_db
COPY init.js /docker-entrypoint-initdb.d/