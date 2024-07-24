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
3. Run `docker compose up db` to start the DB server. Wait until the message "database is ready to accept connections". Then, press CTRL-C to stop the container
4. On a new terminal, run the migrations by running `docker exec -it autohaven-web-1 python manage.py migrate`
5. Run `docker compose up` to start all the containers (DB, Web and Adminer)
6. You should see the logs from all servers in your terminal. This will configure a PostgreSQL database with the credentials defined previously. See [](#credentials) for more details.
7. Once ready, you should see a message similar to `Starting development server at http://0.0.0.0:8000/`. Do not use this URL to access the local web server but http://localhost:8000/ to avoid hosts restrictions
8. If everything is correct, you should see Django welcome screen or the project index once it's implemented. Happy coding!

### Windows

1. Create/edit a .env file as described in [Credentials](#credentials).
2. Open a terminal and navigate to the `./autohaven` directory.
   - You can use `cd autohaven` from a VS code terminal to do this if using powershell.
3. Run `docker compose up db` to start the DB server. Wait until the message "database is ready to accept connections". Then, press CTRL-C to stop the container
4. Run `docker compose up` to start all the containers (DB, Web and Adminer)
5. On a new terminal, run the migrations by running `docker exec -it autohaven-web-1 python manage.py migrate`
6. You should see the logs from all servers in your terminal. This will configure a PostgreSQL database with the credentials defined previously. See [](#credentials) for more details.
7. Once ready, you should see a message similar to `Starting development server at http://0.0.0.0:8000/`. Do not use this URL to access the local web server but http://localhost:8000/ to avoid hosts restrictions
8. If everything is correct, you should see Django welcome screen or the project index once it's implemented. Happy coding!

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

There are 3 main services and a helper service included in the [compose.yaml](./autohaven/compose.yaml) file.

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

- This service uses the image described in the Docker file and starts the dev server using the `python manage.py runserver 0.0.0.0:8000` command to run the web server in the container. It uses the `depends_on` to wait until the DB server is running to connect to the database.
- Docker volume system allows to mount the [/autohaven/](/autohaven/) folder to `/code` inside the container so it has access to the project Python code and also supports hot-reload as expected.
- This service does not answer requests from the host system directly but rather through the [nginx server](#static) (static service) that is included also in the docker setup.

#### Static

- This service uses a [NGINX](https://nginx.org/) web server [docker image](https://hub.docker.com/_/nginx) to host the static and user uploaded files since the project now runs by default with the `DEBUG` setting flag set to `False`, which means Django no longer hosts the static files and media files for us. Therefore, nginx is serving these files. The [/autohaven/nginx.conf](/autohaven/nginx.conf) holds the used nginx configuration which is mounted into the container using the `volumes`configuration from the docker compose file ([/autohaven/compose.yaml](/autohaven/compose.yaml)) to mount the static files and uploaded files folder as well.
- It also acts as a proxy web server to allow the host system to access the django web app. It does so by replicating all the requests as described in https://nginx.org/en/docs/beginners_guide.html#proxy.

### Resources

This docker set up is based on the one available at https://github.com/docker/awesome-compose/tree/master/official-documentation-samples/django/

# Design

# Development

This section contains information about relevant topics regarding development practices and guidelines

## Migrations

Migrations provide way of tracking changes to data models during the project lifetime. This means it's possible to automate tables creation, data loading and database modifications. This is achieved via migration scripts present in the `./autohaven/autohaven_app/migrations/` folder. For instance, initial scripts handle tables creation and relationships across model [0001_initial.py](/autohaven/autohaven_app/migrations/0001_initial.py) creates the Listing, ListingImage and Offer models tables and [0001_listing_body_type.py](/autohaven/autohaven_app/migrations/0001_listing_body_type.py) adds the field `body_type` to the Listings table.

To learn more about the migrations workflow, go to https://docs.djangoproject.com/en/5.0/topics/migrations/#workflow.

### Commands

_Note:_ Before running any of the following commands, make sure the web container is running. You can start it using `docker compose up`

- To check the current pending migrations, run `docker exec -it autohaven-web-1 python manage.py showmigrations`
- To apply the pending migrations, run `docker exec -it autohaven-web-1 python manage.py migrate`
- To automatically create new migrations to sync the current database tables with the model specification, run `docker exec -it autohaven-web-1 python manage.py makemigrations`
- To display the SQL statements that would run as a result of applying the migrations, use `docker exec -it autohaven-web-1 python manage.py slqmigrate`

## Database Models

<!-- TODO: Add reference to the Entity Relationship Model created before -->

# [License](/LICENSE)
