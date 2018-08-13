# webstats_docker

This is the dockerized version of [webstats repository](https://github.com/xaratustrah/webstats).

#### Notes
It is usually desired to have complete isolation between the host and container(s). If you feel the need to run commands on the host from inside a container, then something must be changed in your overall architecture, as this is really not the way things should be designed.

Still deploying docker applications is very attractive as everything is easily configured and you might still want to enjoy docker even for small applications that have strong bonds to the host machine, like a physical hardware connected to it, say for a weather station or a robot. Also `webstats` needs to run system commands on the computer with the GPU hardware and its drivers.

The most secure way of accomplishing this is of course to connect to the host from the container using `ssh`. As you can see in the `Dockerfile` this can be done by using a key authorization. The user name is given via environment variable at the deploy time.

The ssh terminal connection needs to keep quiet since otherwise the resulting output can not be parsed in the web application:

    ssh -o LogLevel=QUIET -o StrictHostKeyChecking=no -tt -l $DOCKERHOST_USER $DOCKERHOST COMMANDS

prevents SSH from printing errors like:

    Pseudo-terminal will not be allocated because stdin is not a terminal.

and

    connection to x.y.z closed.

and also asking if you are sure to connect to a new host when ran for the first time.

#### Starting

You should first start the swarm node:

    docker swarm init


then you can use the deploy script:

    ./deploy.sh
