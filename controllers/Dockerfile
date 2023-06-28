FROM cyberbotics/webots.cloud:R2023b-ubuntu22.04-numpy

# Additional dependencies for the utils folder
RUN apt-get update && apt-get install -y \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*
RUN pip3 install --upgrade pip && \
    pip3 install --root-user-action=ignore --no-cache-dir \
    opencv-python \
    scipy \
    ahrs

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

# Entrypoint command to launch default Python controller script
# (In shell form to allow variable expansion)
WORKDIR /usr/local/webots-project/controllers/participant
ENTRYPOINT python3 -u participant.py
