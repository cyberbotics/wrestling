FROM benjamindeleze/webots-test:R2023b-cloud
# FROM cyberbotics/webots.cloud:R2023b

# Copy all the competition files into a project folder
# in webots.yml this folder is referenced in the "dockerCompose" field to be used by the theia IDE when testing the benchmark online
ENV USERNAME=default
RUN mkdir -p /usr/local/webots-project
COPY . /usr/local/webots-project

