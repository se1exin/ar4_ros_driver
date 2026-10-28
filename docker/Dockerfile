FROM ros:jazzy as builder

WORKDIR /ar4_ws
RUN mkdir -p /ar4_ws/src && \
  git clone https://github.com/ycheng517/ar4_ros_driver.git src

RUN apt update
RUN rosdep update
RUN rosdep install --from-paths src --ignore-src -r -y


FROM builder

SHELL ["/bin/bash", "-c"]

WORKDIR /ar4_ws
COPY . /ar4_ws/src

RUN source /opt/ros/jazzy/setup.bash && colcon build --symlink-install

COPY ./docker/entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
