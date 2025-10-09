# Content Scheduler App API

This repository contains the Python Application Programming Interface that will be used by the Content Scheduler Web Application
to manipulate and query data within the PostGreSQL database. 

In order to run this API locally:
1. Click the Green button at the top-right of the repository's window filled with the text, "Code."
2. You may either use the HTTPS or SSH protocol with the given link, copy that link.
3. In your terminal, run the command: `git clone <HTTPS or SSH Link>`
4. This will create a new directory within your current working directory where you have run the command.
5. In your terminal, change directories to the new ContentSchedulerAPI directory.
6. You may switch to any branch found listed after `origin/<branch name>`

You may use whichever interactive development environment that you choose. In my case, I am developing this API using VSCode's IDE. Therefore, I run the `code .` command after I changed to the directory containing this repository. 

This is the current working entity relationship diagram. This diagram lists all of the resources that will be stored within the PostGreSQL database as well as the properties that will be tracked on those resources:
https://dbdiagram.io/d/Content-Scheduler-68e7256cd2b621e422f7438d

Once the API is successfully cloned, there are still a few more steps necessary to get things rolling.
1. There is an included `requirements.txt` file. This contains all of the dependencies required in this API
2. Create a virtual environment within the API project.
   (a) Run the command `python3 -m venv <filepath to new virtual environment>` MacOS/Linux
   (b) Run the command `python3 -m venv <filepath to new virtual environment>` Windows
3. Run the command `pip install -r requirements.txt`. This will install of the required dependencies.

You have successfully installed all of the project's dependiences. There is yet one more step
This API interacts with a PostGreSQL database. You will first have to install PostGreSQL on locally to your computer.
The steps I took for Linux were:
1. `sudo apt update` Updates Linux shell
2. `sudo apt install postgressql postgresql-contrib` Installs PostGreSQL database
3. `sudo -u postgresql psql` Starts PostGreSQL with postgresql superuser

Inside of the PSQL prompting:
1. `CREATE DATABASE <your database name>;`
2. `CREATE USER <your username> WITH PASSWORD <your password>;`
3. `GRANT ALL PRIVILEGES ON DATABASE <your database name> TO <your username>;`
4. `CREATE SCHEMA content_scheduler;` This part is necessary, I have added a schema name to this database, and will be read during it's creation
   
These commands will create for you a PostGreSQL user and password locally, it will not interfere with anything remote. The username and password will be used later in the creation of the connection string from the API to the PSQL database.

The API and PostGreSQL database have both been initialized, but now we need to create a global environment variable that contains information to connect to the PSQL database from the Python API
Here is the template:
`DATABASE_URL=postgresql://<your username>:<your password>@localhost:5432/<your database name>`

Now that we have the connection string, we can use the Alembic's first version to initialize the PostGreSQL database with all tables, resources, and columns
`alembic upgrade head`

You can also view this information before committing it by running:
`alembic upgrade head --sql`

To ensure that the API is running and the FastAPI's endpoints are working run the uvicorn server:
`uvicorn content_scheduler_app.main:content_scheduler --reload`

You should see the message that the API is healthy. You may also swap to the endpoint `/users` to retrieve a list of users from the database
