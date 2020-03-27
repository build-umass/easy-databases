# Easy Postgres With Docker [WIP]
## Quick Setup
**It is recommended you read the entire README.** Reading it won't take that long, and you will get useful information that will make developing faster in the future.

First, install Docker.

**Helpful Commands/Stuff for Installing Docker on Linux**:
- Install Docker with your package manager
- `sudo usermod -a -G docker <your username>`
- Might have to do: `newgrp docker`
- `sudo systemctl start docker.service`
- `sudo systemctl enable docker.service`
- You might need to restart the docker service/relogin your user account.

Download manage.py (the other files in this repo aren't needed) and try the following commands (on Windows use `python3 manage.py` instead of `./manage.py`):

**Start**: `./manage.py start`  
**Stop**: `./manage.py stop`  
**Connect**: `psql -h localhost -p 5432 -U dev_user -d dev_db`

Now, you want to build our container. Please note that you only need to build it once!
The tag is customized for our image, so make sure you copy the code below for correctness.

**Build**: `docker build -t postgres-image .`

## Summary
This Dockerfile specifies a container that builds upon the default "postgres" container in Docker Hub.

The resulting container lets developers easily use Postgres on their local machines while developing without having to install Postgres the normal way.

This container should not be used in production because it has hardcoded users/passwords to make setup easier and to establish convention.

## Usage
The Postgres database in this container has the following roles/databases:
- Admin
    - Username: admin_user
    - Password: admin
- Normal
    - Username: dev_user
    - Password: dev

There are 2 databases in the Postgres instance:
- admin_db
- dev_db

Developers should use the user "dev_user" and the database "dev_db".

Normally, the Postgres admin user is "postgres" and the default database is "postgres".
Thus, this container breaks convention. However, by making the roles more explicit, there should be less confusion overall.

Data is not persistent inside of containers. Think of a container as a template (like a class). Starting a container merely creates an instance of that class. Stopping a container deletes the instance. Thus, the state of your Postgres database must be stored inside of a Docker volume.

Postgres uses a folder called PGDATA to store all relevant information. PGDATA equals "/var/lib/postgresql/data" on Linux. Thus, to persist the state of the Postgres instance, a Docker volume must be bound to the location of PGDATA.

- If the user does not provide a volume the container will create an empty volume and bind it to PGDATA. Initialization scripts will be run, making the volume non-empty. This volume can be found with `docker volume ls`.
- If the user binds an empty volume to PGDATA, initialization scripts will run, making the volume non-empty.
- If the user binds a non-empty volume to PGDATA, no initialization scripts will run since the database state will be inside PGDATA.

Therefor, the recommended procedure is to:
1. Start the container with an empty volume, *V*, bound to PGDATA. Initialization will occur and *V* will be used as a PGDATA folder.
2. In the future, when you want to use your database again, restart the container with PGDATA bound to *V*, which stores the state of your database.

You can theoretically have multiple volumes, each with different files. When you want to run a given Postgres instance, start the container and bind it to a given volume.

### Commands
**Create and Start Container From Image**: `docker run --rm --volume PGDATA:/var/lib/postgresql/data -d --name pg_docker -p 5432:5432 --ip localhost <image tag>`
- `--rm` Remove this container after it is stopped (for example, with `docker stop <container name/hash>`). Restarting the database will require running the original command again instead of merely running `docker start <container name/hash>`
- `--volume PGDATA:/var/lib/postgresql/data` Bind the Docker volume "PGDATA" to the directory `/var/...` in the container. If the volume "PGDATA" does not exist, create it.
- `-d` Run container in background and print container ID.
- `--name pg_docker` Give the container a name, so you can use commands, like `docker stop` without having to use the container id.
- `-p 5432:5432` Bind port 5432 on the host to port 5432 on the container, which is the default port that Postgres listens on. The syntax is HOST_PORT:CONTAINER_PORT
- `-- ip localhost` Set the container's ip address to localhost. By default, it is 0.0.0.0. Thus, programs can connect to the Postgres database at `localhost:5432` instead of `0.0.0.0:5432`.
- `<image tag>` The unique tag of that will identify the container.

**Connect to the Postgres Database**: `psql -h localhost -p 5432 -U dev_user -d dev_db`
- `-p 5432` This flag is optional since by default psql will use port 5432.

## Technical Details
The normal "postgres" container in Docker Hub uses environment variables to initialize the database. For example, `POSTGRES_USER` determines the username of the Postgres super user.


Of course, if the PGDATA data folder is non-empty (because it has been bound to a non-empty Docker volume), then these environment variables are ignored since the username of the Postgres super user will be stored in the PGDATA folder.

This container presets the value of the environment variables.

The normal "postgres" container also runs SQL scripts in a specific folder in the container (once again, these scripts are run only if the PGDATA folder is empty because it has not been bound to a non-empty Docker volume). This container adds a SQL script to that folder.