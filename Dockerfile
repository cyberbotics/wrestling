FROM cyberbotics/webots.cloud:R2023a-ubuntu20.04

# Copy all the benchmark files into a project folder
# in webots.yml this folder is referenced in the "dockerCompose" field to be used by the theia IDE when testing the benchmark online
RUN mkdir -p /usr/local/webots-project
COPY . /usr/local/webots-project
