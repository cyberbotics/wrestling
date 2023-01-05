FROM cyberbotics/webots.cloud:R2023a-ubuntu20.04

# Copy all the benchmark files into a project folder
# in webots.yml this folder is referenced in the "dockerCompose" field to be used by the theia IDE when testing the benchmark online
RUN mkdir -p /usr/local/webots-project
COPY . /usr/local/webots-project

# The world file path is extracted from webots.yml and is given by the build-arg:
ARG WORLD_PATH
ENV WORLD_PATH=${WORLD_PATH}

# If called with no arguments, launch in headless mode
# (for instance, on the simulation server of webots.cloud, the GUI is launched to stream it to the user and a different command is used)
# - Launching Webots in shell mode to be able to read stdout from benchmark_record_action script
CMD xvfb-run -e /dev/stdout -a webots --stdout --stderr --batch --mode=realtime --no-rendering /usr/local/webots-project/${WORLD_PATH}
