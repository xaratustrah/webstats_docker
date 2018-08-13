# webstats_docker

This is the dockerized version of [webstats repository](https://github.com/xaratustrah/webstats).

#### Notes
`webstats` needs to run system commands on the computer with the GPU hardware. This is in contrast to the concept of the docker containers, since there it is desired to have complete  isolation between the host and container. If you really need to run commands on the host from inside a container, then something must be changed in your overall architecture, as this is really not the way things should be designed.

But in a small application, like a weather station running on a raspberry pi, you may still be interested in doing this. The most secure way is of course to connect to the host from the container using `ssh`. As you can see in the `Dockerfile` this can be accomplished by using a key authorization. The user name is given via environment variable at the deploy time.

The ssh connection in the script:

    ssh -o LogLevel=QUIET -o StrictHostKeyChecking=no -tt -l $DOCKERHOST_USER $DOCKERHOST

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
