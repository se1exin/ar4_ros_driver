# AR4 ROS Driver

ROS 2 driver of the AR4 robot arm from [Annin Robotics](https://www.anninrobotics.com).
Tested with ROS 2 Iron on Ubuntu 22.04. This is a refresh of
[ar3_core](https://github.com/ongdexter/ar3_core).

- [Overview](#Overview)
- [Installation](#Installation)
- [Usage](#Usage)

Video Demo:

[![AR4 ROS 2 Driver Demo](http://img.youtube.com/vi/XJCrfrW7jXE/0.jpg)](https://www.youtube.com/watch?v=XJCrfrW7jXE "AR4 ROS 2 Driver Demo")

## Overview

- **ar_description**
  - Hardware description of arm, urdf etc.
- **ar_hardware_interface**
  - ROS interface for the hardware driver, built on the ros2_control framework
  - Manages joint offsets, limits and conversion between joint and actuator messages
  - Handles communication with the motor controllers
- **ar_microcontrollers**
  - Firmware for the motor controller ie. Teensy
- **ar_moveit_config**
  - MoveIt module for motion planning
  - Controlling the arm through Rviz
- **ar_gazebo**
  - Simulation on Gazebo

## Installation

- Install [ROS 2 Iron](https://docs.ros.org/en/iron/Installation.html) for Ubuntu 22.04
- Clone this repository:
  ```bash
  git clone https://github.com/ycheng517/ar4_ros_driver
  ```
- Install workspace dependencies:
  ```bash
  rosdep install --from-paths . --ignore-src -r -y
  ```
- Build the workspace:
  ```bash
  colcon build
  ```
- Source the workspace:
  ```bash
  source install/setup.bash
  ```
- Enable serial port access if you haven't already done so:
  ```bash
  sudo addgroup $USER dialout
  ```
  You will need to log out and back in for changes to take effect.

### Firmware Flashing

The Teensy Arduino sketch provided in [ar_microcontrollers](./ar_microcontrollers/)
is compatible with the default hardware. To flash it, follow the same
procedure as specified in [AR4 Robot Setup](https://www.youtube.com/watch?v=OL6lXu8VU4s).

### Running in Docker Container

A docker container and run script has been provided that can be used to run the
robot and any GUI programs. It requires an NVIDIA GPU, and the
[NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html)
to be installed. Then you can start the docker container with:

```bash
docker build -t ar4_ros_driver .
./run_in_docker.sh
```

## Usage

There are two modules that you will always need to run:

1. **Arm module** - this can be for either a real-world or simulated arm

   - For controlling the real-world arm, you will need to run the `ar_hardware_interface` module
   - For the simulated arm, you will need to run the `ar_gazebo` module
   - Either of the modules will load the necessary hardware descriptions for MoveIt

2. **MoveIt module** - the `ar_moveit_config` module provides the MoveIt interface and RViz GUI.

The various use cases of the modules and instructions to run them are described below:

---

### Basic Demo in RViz
To preview the robot model and it's joints, run the following across 3 terminals:

Start the state publisher:
```
ros2 launch ar_description robot_state_publisher.launch.py
```

Start the joint state publisher UI, which you can use to manipulate each joint of the robot model
```
ros2 run joint_state_publisher_gui joint_state_publisher_gui
```

Start RViz and open the `rviz` config file located at `ar_description/ar_macro.rviz`.
```
rviz2
```


### MoveIt Demo in RViz

If you are unfamiliar with MoveIt, it is recommended to start with this to explore planning with MoveIt in RViz. This contains neither a real-world nor a simulated arm but just a model loaded within RViz for visualisation.

- The robot description, moveit interface and RViz will all be loaded in the single demo launch file
  ```
  ros2 launch ar_moveit_config demo.launch.py
  ```

---

### Control real-world arm with MoveIt in RViz

Start the `ar_hardware_interface` module, which will load configs and the robot description:

```bash
ros2 launch ar_hardware_interface ar_hardware.launch.py \
  calibrate:=True
```

Notes:

- Calibration is required after flashing firmware to the Teensy board, and
  power cycling the robot and/or the Teensy board. It can be skipped in subsequent
  runs with `calibrate:=False`.
- Serial port of the Teensy board can be specified with the following launch
  argument: `serial_port:=/dev/ttyACM0`.

Start MoveIt and RViz:

```bash
ros2 launch ar_moveit_config ar_moveit.launch.py
```

You can now plan in RViz and control the real-world arm. Joint commands and joint states will be updated through the hardware interface.

---

### Control simulated arm in Gazebo with MoveIt in RViz

- Start the `ar_gazebo` module, which will start the Gazebo simulator and load the robot description
  ```
  ros2 launch ar_gazebo ar_gazebo.launch.py
  ```
- Start Moveit and RViz
  ```
  ros2 launch ar_moveit_config ar_moveit.launch.py use_sim_time:=true
  ```
  You can now plan in RViz and control the simulated arm.
