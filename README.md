# autohaven

A Django project for the AutoHaven website, a sample project for the Software Development - course

# Development Environment Set up

## Requirements

- Linux, Mac or Windows PC.
- [Docker Desktop](https://docs.docker.com/desktop/) for the corresponding platform.
  - You can verify your Docker Installation using `docker run -d -p 8080:80 docker/welcome-to-docker` and accessing http://localhost:8080 on your browser.

## Set Up

> [!IMPORTANT]  
> Setting credentials after the initial set up is possible but troublesome and not covered currently in this guide. Make sure to set your desired credentials before first run to avoid issues.

### Credentials

Before setting up your local environment, you should set the desired DB name, user and password. This can be done by creating/editing the [./autohaven/.env](./autohaven/.env) file. It's not compulsory to do so for setting up a dev environment.

Create a file [./autohaven/.env](./autohaven/.env) with the following contents:

```bash
# Change if desired
POSTGRES_NAME=autohaven
POSTGRES_USER=autohaven
POSTGRES_PASSWORD=changeme
```

### Mac OS

1. Create/edit a .env file as described in [Credentials](#credentials).
2. Open a terminal and navigate to the `./autohaven` directory.
   - You can use `cd autohaven` from a VS code terminal to do this.
3. Run `docker compose up` to start the DB server and Web server.
4. You should see the logs from both servers in your terminal. This will configure a PostgreSQL database with the credentials defined previously. See [](#credentials) for more details.
5. Once ready, you should see a message similar to `Starting development server at http://0.0.0.0:8000/`. Do not use this URL to access the local web server but http://localhost:8000/ to avoid hosts restrictions
6. If everything is correct, you should see Django welcome screen or the project index once it's implemented. Happy coding!

### Windows

1. Create/edit a .env file as described in [Credentials](#credentials).
2. Open a terminal and navigate to the `./autohaven` directory.
   - You can use `cd autohaven` from a VS code terminal to do this if using powers.
3. Run `docker compose up` to start the DB server and Web server.
4. You should see the logs from both servers in your terminal. This will configure a PostgreSQL database with the credentials defined previously. See [](#credentials) for more details.
5. Once ready, you should see a message similar to `Starting development server at http://0.0.0.0:8000/`. Do not use this URL to access the local web server but http://localhost:8000/ to avoid hosts restrictions
6. If everything is correct, you should see Django welcome screen or the project index once it's implemented. Happy coding!

To obtain a more in-depth explanation of the docker set up, see [Docker Setup](#docker-setup)

### Troubleshooting

- Make sure to read the logs from the service containers to look for possible errors or problems during the set up process.
- In case the DB is not property iniatialized, it is possible to reset it to start from scratch. See [Resetting the DB](#resetting-the-db)
- Check there are no other applications using the ports 8000 (Web), 8080 (Adminer) or 5432 (DB)

#### Resetting the DB

**Note: This action is not reversible!**
If required, the DB can be reset by deleting the [/autohaven/data/db](/autohaven/data/db) directory. After doing this, next time the DB container starts it will init the db again recreating the files.

# Project Structure Overview

## Docker Setup

Docker is being used in this project to:

- Improve dev quality of life by ensuring a common experience in all platforms
- Avoid issues regarding installing dependencies
- Dependency pinpoint
- Orquestrate project resources (DB and Web server)

To achieve this, two files are required:

- [Dockerfile](./autohaven/Dockerfile): This file describes the required steps to create a container for the main web application. It starts from a clean Python docker image and installs the Python dependencies specified at the requirements.txt file.
- [compose.yaml](./autohaven/compose.yaml): This file describes the services required to get the web application running in the dev environment.

### Services

There are 2 main services and a helper service included in the [compose.yaml](./autohaven/compose.yaml) file.

#### DB

- This service uses a [PostgreSQL](https://www.postgresql.org/) [docker image](https://hub.docker.com/_/postgres) that runs a database server locally on port 5432. On first run, it creates a default database and database user using environment variables (POSTGRES_USER, POSTGRES_PASSWORD).

- Data from the database is stored in the [/autohaven/data/db](/autohaven/data/db) folder. This folder is excluded from the repository as it's created everytime a new dev environment is set up. The DB can be forced to reset by deleting the contents of this folder.

- A healthcheck for this service is established to determine when the server is ready to accept connections from the web server.

#### Adminer

- Adminer is a Web DB management tool that can be used to easily inspect the contents of the database if required. It runs on port 8080 so it's available to use on http://localhost:8080/. To log in into the DB using adminer use the following input in the web form:
  - System: PostgreSQL
  - Server: db
  - Username: Username set during DB initialization.
  - Password: Password set during DB initialization.
  - Database: Database name set during DB initialization.

#### Web

- This service uses the image described in the Docker file and starts the dev server using the `python manage.py runserver 0.0.0.0:8000` command to run the web server in the container. It exposes port 8080 to the host system to provide access and uses the `depends_on` to wait until the DB server is running to connect to the database.
- Docker volume system allows to mount the [/autohaven/](/autohaven/) folder to `/code` inside the container so it has access to the project Python code and also supports hot-reload as expected.

### Resources

This docker set up is based on the one available at https://github.com/docker/awesome-compose/tree/master/official-documentation-samples/django/

# Design

## Database Models

<!-- TODO: Add reference to the Entity Relationship Model created before -->

# [License](/LICENSE)
