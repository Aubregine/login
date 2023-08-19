### REST API

# Installation

To launch the servers, run the launch.bat file
(you can read the file before running it, to ensure that there is no malicious code inside)

The batch file uses pipenv, make sure pipenv is installed on your machine.

To launch the dockerized version, run the launch_dockerized.bat file instead.
Note that the containers will delete themselves when exited (with Ctrl+C on the terminal), but not when killed (with the close button on the terminal window). If you kill the containers, you will have to delete them manually with `docker rm <container_name>` or using Docker Desktop.

# Usage

The User REST API is available at http://localhost:3203
The other microservices are available at http://localhost:3200, 3201 and 3202, but they do not have an interface

The user homepage allows you to create a user, get the user's infos, get the bookings of a user, and get a list of movies that the user has booked.

You can navigate to the other microservices' homepages by clicking on the links on the app bar.
You can also send custom get/post/whatever request to the microservices using a tool like Postman.
