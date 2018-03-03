#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include <sensor_msgs/Joy.h>
#include "std_msgs/String.h"
#include "std_msgs/Empty.h"
#include "std_msgs/Bool.h"
#include "std_srvs/Empty.h"
#include <stdio.h>
#include <termios.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/time.h>

#include <ctime>
#include <ratio>
#include <chrono>
#include <utility>
#include <thread>
#include <chrono>
#include <functional>
#include <atomic>

// using namespace sensor_msgs;
// using namespace stereo_msgs;
// using namespace message_filters;
// using namespace cv;
using namespace ros;
using namespace std::chrono;

void changemode(int);
int  kbhit(void);

ros::Publisher drift_pub;

ros::Publisher vel_pub_;
  
ros::Publisher takeoff_pub_;
ros::Publisher land_pub_;
ros::Publisher reset_pub_;

ros::Subscriber teleop_sub_;


void teleopCallback(const std_msgs::String::ConstPtr& msg)
{
  geometry_msgs::Twist twist;
  
  bool takeoff_pressed = false;
  bool land_pressed = false;
  bool reset_pressed = false;
  
  twist.linear.x = 0;
  twist.linear.y = 0;
  twist.linear.z = 0;
  twist.angular.z = 0;
  
  std::string command = msg->data.c_str();
  
  if (command.compare("w") == 0) {
    twist.linear.x = 0.3;
  }
  if (command.compare("s") == 0) {
    twist.linear.x = -0.3;
  }
  if (command.compare("z") == 0) {
    twist.linear.y = 0.3;
  }
  if (command.compare("c") == 0) {
    twist.linear.y = -0.3;
  }
  
  if (command.compare("i") == 0) {
    twist.linear.z = 0.3;
  }
  if (command.compare("k") == 0) {
    twist.linear.z = -0.3;
  }
  if (command.compare("a") == 0) {
    twist.angular.z = 0.3;
  }
  if (command.compare("d") == 0) {
    twist.angular.z = -0.3;
  }
  // if (command.compare("o") == 0) {
   //  twist.linear.x = 0.3;
   //  twist.linear.z = 0.2;
  // }
  // if (command.compare("u") == 0) {
   //  twist.linear.x = -0.3;
   //  twist.linear.z = -0.2;
  // }
  
  if (command.compare("h") == 0) {
    twist.linear.x = 0;
    twist.linear.y = 0;
    twist.linear.z = 0;
    twist.angular.z = 0;
  }


  
  std_msgs::Empty myMsg;
  
  if ((command.compare("e") == 0) && !(takeoff_pressed)){
  takeoff_pub_.publish(myMsg);
  takeoff_pressed = true;
  }
  if ((command.compare("e") == 0) && takeoff_pressed){
  vel_pub_.publish(twist);
  }
  
  if ((command.compare("q") == 0) && !(land_pressed)){
  land_pub_.publish(myMsg);
  land_pressed = true;
  }
  if ((command.compare("q") == 0) && land_pressed){
  vel_pub_.publish(twist);
  }
  
  if ((command.compare("r") == 0) && !(reset_pressed)){
  reset_pub_.publish(myMsg);
  reset_pressed = true;
  }
  if ((command.compare("r") == 0) && reset_pressed){
  vel_pub_.publish(twist);
  }
  
  vel_pub_.publish(twist);
  
}

int main(int argc, char** argv)
{
  ros::init(argc, argv, "teleop_key");

  ros::NodeHandle nh_;
  drift_pub = nh_.advertise<std_msgs::String>("key_command", 1000);

  vel_pub_ = nh_.advertise<geometry_msgs::Twist>("bebop/cmd_vel", 1);
  takeoff_pub_ = nh_.advertise<std_msgs::Empty>("bebop/takeoff", 1);
  land_pub_ = nh_.advertise<std_msgs::Empty>("bebop/land", 1);
  reset_pub_ = nh_.advertise<std_msgs::Empty>("bebop/reset", 1);
  teleop_sub_ = nh_.subscribe<std_msgs::String>("key_command", 10, &teleopCallback);

  ros::spin();

  return 0;
}
