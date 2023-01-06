<span id="title">

# Humanoid Robot Wrestling Competition

</span>

[![webots.cloud - Competition](https://img.shields.io/badge/webots.cloud-Competition-007ACC)][1]

<span id="description">

This competition focuses on the development of advanced humanoid robot control software for a wrestling game. It relies on a calibrated simulation model of the NAO robot, running in the Webots simulator with realistic physics, sensor and actuator simulation.

</span>

Being spectacular and fairly easy to get started with, this competition aims at gathering a large number of competitors, both on-site and remotely. The fully open-source competition software stack was designed to be re-used as a template for other simulation-based robot competitions.

![Webots screenshot](preview/thumbnail.jpg "Webots screenshot")

## Competition Information

<span id="information">

- Difficulty: Master or PhD
- Robot: NAO
- Programming Language: any
- Commitment: a few weeks

</span>

## Important Dates

| date               | description                                      |
|--------------------|--------------------------------------------------|
| January 10th, 2023 | registration opens and qualification games start |
| May 23rd, 2023     | selection of the best 32 teams                   |
| **May 30th, 2023** | **1/16 finals**                                  |
| **May 31th, 2023** | **1/8 finals**                                   |
| **June 1st, 2023** | **1/4 finals**                                   |
| **June 2nd, 2023** | **semifinals, third place game and final**       |

The finals will be broadcasted online in real time.

## Prize

The winning team will receive one Ethereum crypto-currency (priced around USD 1,248 on January 6th, 2023).

## Participation Conditions

Anyone can participate: there is absolutely no restriction on the quality and number of team members.
Participation is free of charge, including the finals.

## Get Started Now

To get started programming your wrestling robot, you will have to:

### 1. Create your own Participant Repository from this Template

[Click here](../../generate) to create your own repository automatically or do it manually by clicking on the green button "Use this template".
If you get a 404 page it's probably because you are not connected to your GitHub account.
- Fill the "Repository name" field with a name for your controller.
- Set the visibility of your repository to "Private" unless you don't care about people looking at your code.
- Finally, click on the green button "Create repository from template".

You should continue reading this document on your **own** repository page and not this one.
**This is important** in order to be able to use the links in the following sections.
Remember that you can open a link in a new tab by middle-clicking the link.

### 2. Add the Organizer as a Collaborator

You can skip this step if you created your repository as "Public" instead of "Private".

- [Click here](../../settings/access) to go to the "Collaborators" setting page. You might need to confirm the access by re-entering your GitHub password.
- You should see a "Manage access" box where you will see the current collaborators of the repo.
Click on the "Add people" and search for "[omichel](https://github.com/omichel)".
When you found the organizer, add him to the repository.

### 3. Modify your Robot Controller

You can now edit your [participant.json](../../edit/main/controllers/participant/participant.json) file to set your name, description and country information and also modify your [main robot controller file](../../edit/main/controllers/participant/participant.py) or create new files in this folder and push the modification to the main branch of your repository.
A series of automated actions will take place in a few seconds.
If everything went well, your repository should appear after some time in the [leaderboard][1] of the competition.
If there was a problem, an [issue](../../issues) will be open automatically on your repository by the organizer.
You will have to read it, fix what is wrong and push the changes to your main branch to re-run the automated verification.

## Rules

The rules of game are implemented in the [wrestling referee supervisor](controllers/wrestling_referee/wrestling_referee.py).
They can be summarized as follow:

A game lasts until one of these two conditions occurs:
- **Knock-out**: If the altitude (along Z axis) of the center of mass of one robot remains below a given threshold for more than 10 seconds, then the other robot is declared the winner and the game is immediately over. This may happen if a robot falls down and cannot recover quickly or if it falls off the ring.
- **Time-out**: If no knock-out happened after 5 minutes, the robot having the greater ring *coverage* is declared the winner and the game is over. In the unlikely case of *coverage* equality, the winner is determined randomly. 

The *coverage* reflects how far a robot has moved inside the ring. It is computed over the time frame of a game from its maximum and minimum positions along the X and Y axes, respectively *X_max*, *X_min*, *Y_max* and *Y_min*, using the following formula:

```python
coverage = X_max + Y_max - X_min - Y_min
```

## Recommendation to Competitors

The earlier you start working on the competition, the better.
Starting early will allow you to compete with others from January 10th with an already pretty good robot controller.
The ranking algorithm will allow a very good robot controller to climp-up to the top of the leader board in one day.
However, in practice, it is recommended to enter the leaderboard rankings as early as possible.
This will allow you to compare your robot controller to others and have time to improve its performance.

## Upcoming Workflow

Starting from January 10th, 2023, games will run on demand and the leaderboard will be updated accordingly.
We will soon publish a series of robot controllers that can serve as examples.
You will be able to store your robot controller program on a private GitHub repository to avoid disclosing it to others.
It will be possible to program the robot in any language (C, C++, Python, Java, ROS 2, etc.) with any library or python module.
In order to achieve this, your GitHub repository should contain a [Dockerfile](controllers/Dockerfile) specifying on which environment your controller should run.

### Ranking System

Each time you will push a commit on your main branch, a series of games will be started on the runner machine.
If you are ranked number 1, no game will take place.
Otherwise, you will first play a game against the competitor ranked just above you in the leaderboard.
If you loose, nothing will be changed in the leaderboard ranking and no further game will be played.
Otherwise, you will swap your position in the leaderboard with the competitor just above you and you will play another game with the competitor just above your new position.
This will be repeated as long as you win until you reach the first rank of the leaderboard.

### Runner Machine Configuration

The runner machine will host a single game at a time.
It will run 3 docker containers:

1. One with Webots and the wrestling supervisor.
2. One with the controller of the red player (participant).
3. One with the controller of the blue player (opponent).

Each docker container running a player controller will be allocated 3 virtual CPU cores, 6 GB of RAM and shared access to the GPU hardware. 
The runner machine configuration is the following:
- CPU: [Intel core i7-7700K @ 4.20 Ghz](https://www.cpubenchmark.net/cpu.php?id=2874).
- RAM: 16 GB.
- GPU: [NVIDIA GeForce GTX 1060 3 GB](https://www.videocardbenchmark.net/gpu.php?id=3566).

[1]: https://webots.cloud/run?version=R2022b&url=https%3A%2F%2Fgithub.com%2Fcyberbotics%2Fwrestling%2Fblob%2Fmain%2Fworlds%2Fwrestling.wbt&type=competition "Leaderboard"
