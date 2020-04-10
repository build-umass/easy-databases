# Easy Postgres With Docker [WIP]
## Quick Setup
**Read the entire README.** 

Download the entire repository. If you intend to use only postgres, you may delete the mongo folder. If you intend to use only mongo, you may delete the postgres folder.

The repo offers the following commands (on Windows use `python3 manage.py` instead of `./manage.py`).

## For PostgreSQL:

**Build**: `./manage.py build postgres`

**Start**: `./manage.py start postgres` 

**Stop**: `./manage.py stop postgres`

**Connect/Manage**:
```
docker exec -it <container name, default = postgres_docker> bash
// you are now inside the container
psql -h localhost -p 5432 -U dev_user -d dev_db
//inside psql shell
```

## For MongoDB:

**Build**: `./manage.py build mongo`

**Start**: `./manage.py start mongo` 

**Stop**: `./manage.py stop mongo`

**Connect/Manage**:
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
These are some extra options if you don't want to use the defaults.

Please note that these commands must be put before `build, start, stop`. 

For example: `./manage.py -p 27017:27017 start mongo`.

`-v` or `--volume=` to use a custom volume.

`-n` or `--name=` to give the container a custom name.

`-i` or `--image=` to use a custom image.

`-p` or `--port=` to use a custom host port.

If you are using these options, you should probably just use the Docker command line interface instead of our wrapper script.

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

## Usage

- Build an image with `./manage.py build <postgres/mongo>`. You only need to build an image once.
- Create a container based on an image with `./manage.py run <postgres/mongo>`
- Stop the container with `./manage.py stop <postgres/mongo>`
- Connecting to a database within a container is explained at the top of the README.

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

Data is not persistent inside of containers. Think of an image as a template (like a class). Starting a container merely creates an instance of that image (class). Stopping a container deletes the instance. Thus, the state of your database must be stored inside of a Docker volume.

### Volumes

In the container, Postgres uses a folder "/var/lib/postgresql/data" and Mongo uses the folder /db/data to store all the data that is created in this container for later use (i.e. after we stop the container, and start it again), we must have to create a location on our local machine that is able to retain such data. Hence, we have to bind a location on our local machine, to that directory in the container. Thankfully, Docker has an option to do this for us, by managing the database files on our local machine. Instead of binding a specific directory, Docker will mount a volume for us.

- If the user does not provide a volume the container will create an empty volume named postgres-volume (or mongo-volume for Mongo) and bind it to /var/lib/postgresql/data (or /db/data for Mongo). Initialization scripts will be run, making the volume non-empty. This volume can be found with `docker volume ls`.
- If the user binds an empty volume, initialization scripts will run, making the volume non-empty.
- If the user binds a non-empty volume, no initialization scripts will run since the database state will be inside that volume.

Therefore, the recommended procedure is to:
1. Start the container with an empty volume, *V* (default case would be postgres-volume for postgres, and mongo-volume for mongo), bound to "/var/lib/postgresql/data" or "/db/data" for mongo. Initialization will occur and  will be used as a folder to which data is stored.
2. In the future, when you want to use your database again, restart the container with *V* bound to "/var/lib/postgresql/data" or "/db/data" for mongo, which stores the state of your database.

You can theoretically have multiple volumes, each with different files. When you want to run a given Postgres or Mongo instance, start the container and bind it to a given volume.
