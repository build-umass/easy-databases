# Easy Postgres With Docker [WIP]
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

Data is not persistent inside of containers. Think of a container as a template (like a class). Starting a container merely creates an instance of that class. Stopping a container deletes the instance. Everytime you restart a container, it is wiped clean. Thus, the state of your Postgres database must be stored inside of a Docker volume.

Postgres uses a folder called PGDATA to store all relevant information. The default location of PGDATA is "/var/lib/postgresql/data" on Linux. Thus, to persist the state of the Postgres instance, a Docker volume must be bound to the location of PGDATA. **[TODO: Add more detail]**

Thus, there are 3 scenarios:
- If no Docker volume is bound to PGDATA, then PGDATA will be created on the container and initialization will occur (the default users/databases will be created). When the container is stopped, this folder will be lost.
- If an empty Docker volume is bound to PGDATA, then the volume will be used as the PGDATA folder and initialization will occur, making the volume non-empty.
- If a non-empty Docker volume is bound to PGDATA, then the volume will be used as the PGDATA folder and initialization will be skipped since the volume stores the existing state of the database.

Therefor, the recommended procedure is to:
1. Start this container with an empty Docker volume, *V*. Initialization will occur and *V* will be used as a PGDATA folder.
2. In the future, when you want to use your database again, restart the container and bind it to *V*, which stores the state of your database.

**[TODO: Add the actual commands]**
### Commands
**[TODO: Make commands bind Docker volume]**  
**Create/Start Container**: `docker run -d --name my_pg -p 5432:5432 --ip localhost <container id>`
## Technical Details
The normal "postgres" container in Docker Hub uses environment variables to initialize the database. For example, `POSTGRES_USER` determines the username of the Postgres super user.


Of course, if the PGDATA data folder is non-empty (because it has been bound to a non-empty Docker volume), then these environment variables are ignored since the username of the Postgres super user will be stored in the PGDATA folder.

This container presets the value of the environment variables.

The normal "postgres" container also runs SQL scripts in a specific folder in the container (once again, these scripts are run only if the PGDATA folder is empty because it has not been bound to a non-empty Docker volume). This container adds a SQL script to that folder.