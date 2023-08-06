from asyncio import TimerHandle
import launch
from launch.substitutions import Command
import launch_ros
from launch import EventHandler, LaunchDescription
import sys
from launch_ros.actions import Node
import launch
from launch.actions import (DeclareLaunchArgument, EmitEvent, ExecuteProcess,
                            LogInfo, RegisterEventHandler, TimerAction)
from launch.conditions import IfCondition
from launch.event_handlers import (OnExecutionComplete, OnProcessExit,
                                OnProcessIO, OnProcessStart, OnShutdown)
from launch.events import Shutdown
from launch.substitutions import (EnvironmentVariable, FindExecutable,
                                LaunchConfiguration, LocalSubstitution,
                                PythonExpression)
import time


start_time = time.time()

def generate_launch_description():
    logger = Node(
                package='lulab_sync',
                namespace='lulav',
                executable='logger',
                name='logger'
        )
    dynamics = Node(
                package='lulav_dynamics',
                namespace='lulav',
                executable='lulav_dynamics',
                name='lulav_dynamics',
                output='screen'
        )
    navigation = Node(
            package='lulav_navigation',
            namespace='lulav',
            executable='lulav_navigation',
            name='lulav_navigation',
            output='screen'
        )
    guidance = Node(
            package='lulav_guidance',
            namespace='lulav',
            executable='lulav_guidance',
            name='lulav_guidance',
            output='screen'
        )
    control = Node(
            package='lulav_control',
            namespace='lulav',
            executable='lulav_control',
            name='lulav_control',
            output='screen'
        )
    scheduler = Node(
            package='lulab_sync',
            namespace='lulav',
            executable='scheduler',
            name='scheduler',
            output='screen'
        )
    record = launch.actions.ExecuteProcess(
            cmd=['ros2', 'bag', 'record', '-a'],
            output='screen'
        )
    return LaunchDescription([
        logger,
        dynamics,
        navigation,
        guidance,
        control,
        scheduler,
        record,
        RegisterEventHandler(
            OnProcessExit(
                target_action=dynamics,
                on_exit=[
                    EmitEvent(event=Shutdown(
                        reason='Simulation ended, shutting down')
                    )
                ]
            )
        ),
    ])


def main():
    number_of_runs = 50
    for i in range(number_of_runs):
        try:
            launch_description = generate_launch_description()
            launch_service = launch.LaunchService()
            launch_service.include_launch_description(launch_description)
            launch_service.run()
            print(f"Finished {i+1} runs...")
            time.sleep(5)
        except Exception as e:
            print (e)
            continue



if __name__ == '__main__':
    main()