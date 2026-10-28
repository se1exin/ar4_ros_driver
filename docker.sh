docker run -it \
  -e ROS_STATIC_PEERS=10.1.1.6 \
  --device /dev/ttyUSB0 \
  --device /dev/ttyACM0 \
  -v $(pwd):/ar4_ws/src \
  --net=host \
  ar4_ros_driver ros2 launch annin_ar4_driver driver.launch.py calibrate:=False ar_model:="mk2"
  #ar4_ros_driver ros2 launch annin_ar4_driver driver.launch.py calibrate:=True ar_model:="mk2"
