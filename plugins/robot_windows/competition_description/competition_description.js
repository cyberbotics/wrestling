import RobotWindow from 'https://cyberbotics.com/wwi/R2023b/RobotWindow.js';

window.robotWindow = new RobotWindow();

window.robotWindow.receive = function(message, robot) {
  if (message.startsWith('data:image')) {
    const imageElement = document.getElementById('robot-camera');
    if (imageElement != null)
      imageElement.setAttribute('src', message);
  } else {
    if (message.length > 200)
      message = message.substr(0, 200);
    console.log("Received unknown message for robot '" + robot + "': '" + message + "'");
  }
};
