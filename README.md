# OpenHome

This application allows for registering custom built IoT devices and managing them remotely.

# Running the App

To run the sample, make sure you have `python3`, `python3-flask` and `pip` installed.

Run `pip install -r requirements.txt` to install the dependencies and run `flask run`.
The app will be served at [http://localhost:3000/](http://localhost:3000/).

# Running the App with Docker

To run the sample, make sure you have `docker` installed.

To run the sample with [Docker](https://www.docker.com/), make sure you have `docker` installed.

Rename the .env.example file to .env, change the environment variables, and register the URLs as explained [previously](#running-the-app).

Run `sh exec.sh` to build and run the docker image in Linux or run `.\exec.ps1` to build
and run the docker image on Windows.