# TODO: replace the image with cyberbotics/webots.cloud:R2023a-rev1-ubuntu20.04-numpy when it is available
# FROM leoduggan/webots.cloud-develop:31-01-2023
FROM leoduggan/webots.cloud:master

# Copy all the benchmark files into a project folder
# in webots.yml this folder is referenced in the "dockerCompose" field to be used by the theia IDE when testing the benchmark online
RUN mkdir -p /usr/local/webots-project
COPY . /usr/local/webots-project
