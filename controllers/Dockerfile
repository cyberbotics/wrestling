FROM cyberbotics/webots.cloud:R2023a-ubuntu20.04

# Environment variables needed for Webots
# https://cyberbotics.com/doc/guide/running-extern-robot-controllers#remote-extern-controllers
ENV PYTHONPATH=${WEBOTS_HOME}/lib/controller/python
ENV PYTHONIOENCODING=UTF-8
ENV LD_LIBRARY_PATH=${WEBOTS_HOME}/lib/controller:${LD_LIBRARY_PATH}
ARG WEBOTS_CONTROLLER_URL
ENV WEBOTS_CONTROLLER_URL=${WEBOTS_CONTROLLER_URL}

# Copies all the files of the controllers folder into the docker container
RUN mkdir -p /usr/local/webots-project/controllers
COPY . /usr/local/webots-project/controllers

# The default controller name is extracted from webots.yml and is given by the build-arg:
ARG DEFAULT_CONTROLLER
ENV DEFAULT_CONTROLLER=${DEFAULT_CONTROLLER}

# Entrypoint command to launch default Python controller script
# (In shell form to allow variable expansion)
WORKDIR /usr/local/webots-project/controllers/$DEFAULT_CONTROLLER
ENTRYPOINT python3 -u $DEFAULT_CONTROLLER.py
