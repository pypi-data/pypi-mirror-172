import subprocess
import signal
from subprocess import Popen, PIPE
from datetime import datetime
import time
import sys
import os

class Runner():
    def __init__(self):
        self.start_time = datetime.now().second

    def create_source_underlay_command(self, ros_distro):
         return f"source /opt/ros/{ros_distro}/setup.bash"

    def create_source_overlay_command(self, ws_path):
            return f"source {ws_path}/install/local_setup.bash"

    def create_running_command(self, launch_filename, launch_package=None):
        if launch_package:
            return f"ros2 launch {launch_package} {launch_filename}"
        return f"ros2 launch {launch_filename}"

    def create_stopping_condition(self, topic_or_param="topic", attr_num=0, condition={}):
        if topic_or_param == "topic":
            pass

    def run(self, timeout=5):
        commands = f'{self.create_source_underlay_command("foxy")};\
                     {self.create_source_overlay_command("~/demo_lulav_elbit")};\
                     {self.create_running_command("dynamics_controller.launch.py", "dynamics")}'

        launch = subprocess.Popen(commands, executable='/bin/bash',  text=True, shell=True)
        # position = subprocess.Popen('ros2 topic echo /dynamics/position > ./position', executable='/bin/bash', text=True, shell=True)

        time.sleep(timeout)
        os.killpg(os.getpgid(launch.pid), signal.SIGTERM)
        
def main():
    runner = Runner()
    runner.run()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)




