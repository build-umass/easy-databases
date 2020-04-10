# Easy Databases With Docker
## Quick Setup
**Read the entire README.** 

Download the entire repository. If you intend to use only postgres, you may delete the mongo folder. If you intend to use only mongo, you may delete the postgres folder.

The repo offers the following commands (on Windows use `python3 manage.py` instead of `./manage.py`).

**Build**: `./manage.py build <postgres/mongo>`

**Run**: `./manage.py run <postgres/mongo>` 

**Stop**: `./manage.py stop <postgres/mongo`

**Connect/Manage (Postgres)**:
```
docker exec -it <container name, default = postgres_docker> bash
// you are now inside the container
psql -h localhost -p 5432 -U dev_user -d dev_db
//inside psql shell
```

**Connect/Manage (Mongo)**:
```
docker exec -it <container name, default = mongo_docker> bash
// you are now inside the container
mongo
//inside mongo shell
use <insert database name>
//switch to other db
db.auth(<username>, <password>)
//authenticate for access privileges
```

### Extra Options
manage.py is a wrapper script that calls `docker build`, `docker run`, and `docker stop` with helpful defaults.  
You can override the defaults with command line flags.  
Use `./manage.py <build/run/stop> -h` if you want auto-generated usage instructions.  

Example (override the default port that is passed to `docker run`):
- `./manage.py run mongo --port 3000` (default port on host container is 27017)
- `./manage.py run --port 3000 mongo`

`-v` or `--volume` to use a custom volume. (Default = postgres_volume, mongo_volume)

`-n` or `--name` to give the container a custom name. (Default = postgres_docker, mongo_docker)

`-i` or `--image` to use a custom image. (Default = buildumass/easy-postgres, buildumass/easy-docker)

`-p` or `--port` to use a custom host port. (Default = 5432, 27017)

## Docker Installation:

manage.py requires Docker to be installed. Visit the Docker website for installation information.

**Helpful Commands/Stuff for Installing Docker on Linux**:
- Install Docker with your package manager
- `sudo usermod -a -G docker <your username>`
- Might have to do: `newgrp docker`
- `sudo systemctl start docker.service`
- `sudo systemctl enable docker.service`
- You might need to restart the docker service/relogin your user account.
# Summary

## Dockerfile/Why use Docker

This project has 2 Dockerfiles, one for mongo, one for postgres. Each Dockerfile specifies an image, which is built with `docker build`. Developers can use `docker run` to create a container based on an image (if the image has been built). The containers allow developers to easily use Postgres/Mongo on their local machines without having to install the databases the normal way.

The containers should not be used in production because they have hardcoded users/passwords to make setup easier and to establish convention.

`manage.py` wraps the commands `docker build`, `docker run`, `docker stop` with useful defaults. But, you can always call the commands yourself.

### Databases

Both databases in this container will be initialized with the following roles/databases:
- Admin
    - DB: admin_db
    - Username: admin_user
    - Password: admin
- Normal
    - DB: dev_db
    - Username: dev_user
    - Password: dev

Developers should use the user "dev_user" and the database "dev_db".

Data is not persistent inside of containers. Think of an image as a template (like a class). Creating a container merely creates an instance of that image (class). Stopping a container deletes the instance. Thus, the state of your database must be stored inside of a Docker volume.

### Volumes
[Read this](https://docs.docker.com/storage/)  
[Read this too](https://docs.docker.com/storage/volumes/)

Inside the container's file system, Postgres uses the folder "/var/lib/postgresql/data" and Mongo uses the folder /db/data to store all their data. Containers automatically reset after being stopped, so we need create a location on our local machine that can save the data inside the container for later use (i.e. after we stop the container and start it again). Docker allows us to do this with volumes, which bind a directory on the container to a directory on our local file system. For example, if we bound "/home/username/Desktop" on our host machine to "/var/lib/postgresql/data", then any data Postgres generates inside the container would be saved on our desktop, and any data we save on our Desktop would be readable by Postgres.

When you first run, `./manage.py run <postgres/mongo>`, we tell `docker run` to use the volume named "postgres-volume" (or "mongo-volume" for Mongo) and bind it to /var/lib/postgresql/data (or /db/data for Mongo). Since this volume does not exist, `docker run` will automatically create an empty volume with the name we give it. Since the volume is empty, initialization scripts will run, making the volume non-empty. You can find this volume with `docker volume ls` and use `docker volume inspect [some arguments]` to find the location of the volume on your local file system.

Afterwards, when calling `./manage.py run <postgres/mongo>`, we tell `docker run` to use the volume named "postgres-volume" (or "mongo-volume" for Mongo), but because this volume already exists, `docker run` will use it, instead of creating a new volume. Since the volume is non-empty, initialization scripts will not run.

Therefore, the recommended procedure (which `./manage.py build` and `./manage.py run` do by default) is to:
1. Create a container with an empty volume, *V* (default case would be postgres-volume for postgres, and mongo-volume for mongo), bound to "/var/lib/postgresql/data" or "/db/data" for mongo. Initialization will occur and the volume will be used to store data.
2. In the future, when you want to use your database again, restart the container with *V* bound to "/var/lib/postgresql/data" or "/db/data" for mongo, which stores the state of your database.

You can theoretically have multiple volumes, each with different files. When you want to run a given Postgres or Mongo instance, start the container and bind it to a given volume.
