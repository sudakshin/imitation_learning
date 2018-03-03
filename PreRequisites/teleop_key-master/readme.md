###teleop_key: A simple code to teleoperate Parrot AR.Drone/Bebop/Bebop2 quadcopter.

Prerequisite: ardrone_autonomy(https://github.com/AutonomyLab/ardrone_autonomy) / bebop_autonomy(http://bebop-autonomy.readthedocs.io/en/latest/) as per quadcopter

Can also be tried using Gazebo (https://github.com/dougvk/tum_simulator).

Clone the repo in your ros workspace and do "catkin_make --pkg teleop_key"

Once the autonomy (or simulation) is on, run

rosrun teleop_key teleop_key_pub

Then in different tab, run

rosrun teleop_key teleop_key_sub_bebop (or rosrun teleop_key teleop_key_sub_ardrone)

####Make sure that the focus is on teleop_key_pub tab

Here are the teleop commands --

e -> take off

q -> land

r -> reset

w -> move forward

s -> move backward

a -> move left > z

d -> move right > c

j -> turn left > a

l -> turn right > d

i -> go up (increase altitude)

k -> go down

If no key is pressed, a default 'hover' command will be sent. Change the absolute values in the subscriber code as per requirement (default: 0.3)


catkin build afte making changes