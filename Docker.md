# How to run in a Docker container

Build it via `docker build -t my-image .`

Run it via `docker run -v /path/to/your/token-folder/:/SECRET -d my-image`
/path/to/your/token-folder/ must contain the token.txt file.

Alternative, place it in the root of this repo and build it yourself with removing line 1 
in .dockerignore .