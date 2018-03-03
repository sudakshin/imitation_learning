#include "ros/ros.h"
#include "std_msgs/String.h"
#include <stdio.h>
#include <termios.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/time.h>
#include <sstream>
#include <string>

void changemode(int);
int  kbhit(void);

int count = 0;

char lastCommand = 'h';

int main(int argc, char **argv)
{

  ros::init(argc, argv, "teleop_key_pub");

  ros::NodeHandle n;

 
  ros::Publisher teleop_pub = n.advertise<std_msgs::String>("key_command", 1000);

  ros::Rate loop_rate(10);

  while (ros::ok())
  {
    std_msgs::String msg;
    
    char command = lastCommand;
    
    std::stringstream ss;
    
    changemode(1);
    
    ss << command;
    msg.data = ss.str();
    
    while ( !kbhit() && count == 0)
    {
		  teleop_pub.publish(msg);

      ros::spinOnce();

      loop_rate.sleep();
        
      count++;
	  }
 
	count = 0;
	
    lastCommand = getchar();
 
    changemode(0);
    
  }


  return 0;
}

void changemode(int dir)
{
  static struct termios oldt, newt;
 
  if ( dir == 1 )
  {
    tcgetattr( STDIN_FILENO, &oldt);
    newt = oldt;
    newt.c_lflag &= ~( ICANON | ECHO );
    tcsetattr( STDIN_FILENO, TCSANOW, &newt);
  }
  else
    tcsetattr( STDIN_FILENO, TCSANOW, &oldt);
}
 
int kbhit (void)
{
  struct timeval tv;
  fd_set rdfs;
 
  tv.tv_sec = 0;
  tv.tv_usec = 0;
 
  FD_ZERO(&rdfs);
  FD_SET (STDIN_FILENO, &rdfs);
 
  select(STDIN_FILENO+1, &rdfs, NULL, NULL, &tv);
  return FD_ISSET(STDIN_FILENO, &rdfs);
 
}
